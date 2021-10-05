import axios from 'axios'

export const server = 'http://127.0.0.1:8000'
export const header = {'Content-Type':'application/json'}

export const connect = () => axios.get(`${server}/api/connect`)