// Configuración para Docker - Frontend y Backend en mismo dominio
window.env = {
    API_URL: '/api',  // URL relativa - sin CORS
    DEBUG: false,
    VERSION: '1.0.0'
};

// Función para verificar conectividad de la API
window.checkAPI = async function() {
    try {
        const response = await fetch(`${window.env.API_URL}/health`);
        const data = await response.json();
        console.log('✅ API Status:', data);
        return data;
    } catch (error) {
        console.error('❌ API Error:', error);
        return { status: 'ERROR', error: error.message };
    }
};