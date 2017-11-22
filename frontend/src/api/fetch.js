import axios from 'axios'
import Cookies from 'js-cookie'
import { Message } from 'element-ui'

// 创建axios实例
const service = axios.create({
  baseURL: 'http://10.10.59.42:8004/api/', // api的base_url
  timeout: 10000                  // 请求超时时间
})

// request拦截器
service.interceptors.request.use(config => {
  // Do something before request is sent
  console.log(Cookies.get('token'))
  var token = Cookies.get('token')
  if (token) {
    console.log(config)
    console.log(config.params)
    config.data.token = token
  }
  return config
}, error => {
  // Do something with request error
  console.log(error) // for debug
  Promise.reject(error)
})

// respone拦截器
service.interceptors.response.use(
  response => {
    if (response.data.code === 1) {
      return response.data.data
    } else {
      return Promise.reject(response.data.msg)
    }
  },
  error => {
    console.log('err' + error)// for debug
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
