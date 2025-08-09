// Configuración para producción - Vercel + PythonAnywhere
window.env = {
    API_URL: 'https://sgit.pythonanywhere.com/api',
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