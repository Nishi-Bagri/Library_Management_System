import axios from "axios";

const api = axios.create({
    baseURL: "http://192.168.1.75:8000/api/",
});

// Attach access token to every request
api.interceptors.request.use(
    (config) => {
        const access = localStorage.getItem("access");

        if (access) {
            config.headers.Authorization = `Bearer ${access}`;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

// Refresh access token on 401
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (
            error.response?.status === 401 &&
            !originalRequest._retry
        ) {
            originalRequest._retry = true;

            try {
                const refresh = localStorage.getItem("refresh");

                const res = await axios.post(
                    "http://192.168.1.75:8000/api/token/refresh/",
                    {
                        refresh,
                    }
                );

                // Save the new access token
                localStorage.setItem("access", res.data.access);

                // Retry the original request with the new token
                originalRequest.headers.Authorization = `Bearer ${res.data.access}`;

                return api(originalRequest);

            } catch (err) {
                // Refresh token is invalid or expired
                localStorage.removeItem("access");
                localStorage.removeItem("refresh");
                localStorage.removeItem("role");

                window.location.href = "/";

                return Promise.reject(err);
            }
        }

        return Promise.reject(error);
    }
);

export default api;