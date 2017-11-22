import fetch from './fetch'

const userService = {}

userService.login = function (params) {
  return fetch({
    url: 'user/login',
    method: 'post',
    data: params
  })
}

userService.addUser = function (params) {
  return fetch({
    url: 'user/login',
    method: 'post',
    data: params
  })
}

userService.getUserList = function (params) {
  return fetch({
    url: 'admin/listUser',
    method: 'post',
    data: params
  })
}

userService.getUserInfo = function (params) {
  return fetch({
    url: 'user/getUserInfo',
    method: 'post',
    params: params
  })
}

export default userService
