import axios from 'axios'

const server = 'http://127.0.0.1:8000/api'
const header = {'Content-Type':'application/json'}
export const connect = () => axios.get(`${server}/connect`)
export const userRegister = body => axios.post(`${server}/users/register`, {header, body})
export const userList = () => axios.get(`${server}/users/list`)
export const userDetail = id => axios.get(`${server}/users/${id}`)
export const userRetriever = (key, value) => axios.get(`${server}/users/${key}/${value}`)
export const userModify = body => axios.put(`${server}/users`, {header, body})
export const userRemove = id => axios.delete(`${server}/users/${id}`)
