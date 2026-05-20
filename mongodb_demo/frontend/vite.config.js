import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const mongoApiProxyTarget = process.env.VITE_MONGO_API_PROXY_TARGET || process.env.VITE_API_PROXY_TARGET || "http://localhost:5000";
const mongoAtlasPort = process.env.MONGO_ATLAS_PORT || "5002";
const mongoAtlasApiProxyTarget = process.env.VITE_MONGO_ATLAS_API_PROXY_TARGET || `http://localhost:${mongoAtlasPort}`;
const postgresApiProxyTarget = process.env.VITE_POSTGRES_API_PROXY_TARGET || "http://localhost:5001";

export default defineConfig({
    plugins: [react()],
    server: {
        host: "0.0.0.0",
        port: 3000,
        proxy: {
            "/api/mongo-atlas": {
                target: mongoAtlasApiProxyTarget,
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/mongo-atlas(?=\/|$)/, "/api"),
            },
            "/api/mongo": {
                target: mongoApiProxyTarget,
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/mongo(?=\/|$)/, "/api"),
            },
            "/api/postgres": {
                target: postgresApiProxyTarget,
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/postgres/, "/api"),
            },
            "/api": {
                target: mongoApiProxyTarget,
                changeOrigin: true,
            },
        },
    },
});