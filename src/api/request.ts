import axios from 'axios';
import type { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse } from 'axios';

const request: AxiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://101.43.94.172:3000/api',
    timeout: 300000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// 请求拦截器
request.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        // 在发送请求之前做些什么
        // 例如: 添加token
        const token = localStorage.getItem('token');
        if (token && config.headers) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        // 对请求错误做些什么
        return Promise.reject(error);
    }
);

// 响应拦截器
request.interceptors.response.use(
    (response: AxiosResponse) => {
        // 对响应数据做点什么
        return response.data;
    },
    (error) => {
        // 对响应错误做点什么
        if (error.response) {
            // 处理不同的HTTP状态码
            switch (error.response.status) {
                case 401:
                    // 未授权,可能需要重新登录
                    break;
                case 404:
                    // 请求的资源不存在
                    break;
                case 500:
                    // 服务器错误
                    break;
                default:
                // 处理其他错误
            }
        }
        return Promise.reject(error);
    }
);

export default request;