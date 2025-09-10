import unittest
from collections import defaultdict

from backend.app import app


def _norm_name(name: str) -> str:
	return (name or "").strip().lower()


class SubcategoriasUnicidadTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.client = app.test_client()

	def test_subcategorias_activas_sin_duplicados_global(self):
		resp = self.client.get("/api/subcategorias")
		self.assertEqual(resp.status_code, 200)
		data = resp.get_json()
		# Estructura: [{id, nombre, categoria_id, descripcion, activo}]
		seen = set()
		duplicates = []
		for sc in data:
			# Deben ser solo activas
			self.assertEqual(sc.get("activo"), 1, f"Subcategoria inactiva filtrada: {sc}")
			key = (sc.get("categoria_id"), _norm_name(sc.get("nombre")))
			if key in seen:
				duplicates.append(key)
			seen.add(key)
		self.assertFalse(duplicates, f"Hay duplicados activos por (categoria_id, nombre): {duplicates[:10]}")

	def test_subcategorias_por_categoria_sin_duplicados(self):
		# Descubrir categorias presentes
		resp = self.client.get("/api/subcategorias")
		self.assertEqual(resp.status_code, 200)
		data = resp.get_json()
		categorias = sorted({sc.get("categoria_id") for sc in data if sc.get("categoria_id") is not None})

		# Verificar por cada categoria
		for cat_id in categorias:
			r = self.client.get(f"/api/subcategorias?categoria_id={cat_id}")
			self.assertEqual(r.status_code, 200)
			lista = r.get_json()
			seen = set()
			dups = []
			for sc in lista:
				self.assertEqual(sc.get("activo"), 1)
				key = _norm_name(sc.get("nombre"))
				if key in seen:
					dups.append(key)
				seen.add(key)
			self.assertFalse(dups, f"Duplicados activos en categoria {cat_id}: {dups}")


if __name__ == "__main__":
	unittest.main(verbosity=2)

