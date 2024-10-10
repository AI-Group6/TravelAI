import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://localhost:5000',
})

export const postUser = async (username, password) => {
    await axiosInstance.post('/users', {login: username, password: password});
}

export const checkLogin = async (username, password) => {
    const response =  await axiosInstance.get('/users', {params: {login: username, password: password}});
    return response.data.exists;
}

export const postHistory = async (user_login, title_message, ai_response) => {
    await axios.post('http://localhost:5000/history', {user_login, title_message, ai_response});
}

export const getHistory = async () => {
    const response = await axios.get('http://localhost:5000/history');
    return response;
}
