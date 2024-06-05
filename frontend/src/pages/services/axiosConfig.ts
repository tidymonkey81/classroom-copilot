import axios from 'axios';

// Set base URL globally for Axios
axios.defaults.baseURL = `http://${import.meta.env.VITE_BACKEND_URL}:${import.meta.env.VITE_BACKEND_PORT}`;

export default axios;