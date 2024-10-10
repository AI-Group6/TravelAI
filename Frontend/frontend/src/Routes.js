import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://localhost:5000',
})

export const postUser = async (username, password) => {
    await axiosInstance.post('/users', {username, password});
}

export const getUsers = async () => {
    const response = await axios.get('http://localhost:5000/users');
    return response;
}

export const postHistory = async (user_login, title_message, ai_response) => {
    await axios.post('http://localhost:5000/history', {user_login, title_message, ai_response});
}

export const getHistory = async () => {
    const response = await axios.get('http://localhost:5000/history');
    return response;
}
