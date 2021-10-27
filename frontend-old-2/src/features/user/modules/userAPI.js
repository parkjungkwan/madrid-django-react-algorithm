import axios from 'axios'

export const server = 'http://127.0.0.1:8000'
export const header = {'Content-Type':'application/json'}

export const userRegister = body => axios.post(`${server}/api/users/register`, {header, body})
export const userList = () => axios.get(`${server}/api/users/list`)
export const userDetail = id => axios.get(`${server}/api/users/${id}`)
export const userRetriever = (key, value) => axios.get(`${server}/api/users/${key}/${value}`)
export const userModify = body => axios.put(`${server}/api/users`, {header, body})
export const userRemove = id => axios.delete(`${server}/api/users/${id}`)