import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://localhost:5000',
})

export const postUser = async (username, password) => {
    const response = await axiosInstance.post('/users', {login: username, password: password});
    return response.data.exists;
}

export const checkLogin = async (username, password) => {
    const response =  await axiosInstance.get('/users', {params: {login: username, password: password}});
    return response.data.success;
}

export const postHistory = async (user_login, title_message, ai_response) => {
    const response = await axiosInstance.post('/history', {login: user_login, message: title_message, response: ai_response});
    return response.data.success;
}

export const getHistory = async (username) => {
    const response = await axiosInstance.get('/history', {params: {username: username}});
    return response.data.history;
}
