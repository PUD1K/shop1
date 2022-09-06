import { createStore } from 'vuex'

export default createStore({
  state: {
    cart: {
      items: [],
    },
    isAuthentificated: false,
    token: '',
    isLoading: false,
    username: '',
  },
  getters: {
  },
  mutations: {
    //если в localStorage есть что-то в корзине, то передаем это в state, иначе выполняем обратную процедуру
    initializeStore(state){
      if(localStorage.getItem('cart')){
        state.cart = JSON.parse(localStorage.getItem('cart'))
      }
      else{
        localStorage.setItem('cart', JSON.stringify(state.cart))
      }
      //если в localStorage есть токен, добавляем его в state
      if(localStorage.getItem('token')){
        state.token = localStorage.getItem('token')
        state.isAuthentificated = true
      }else {
        state.token = ''
        state.isAuthentificated = false
      }
    },
    addToCart(state, item){
      //выбрать все товары с айди как у передаваемого в параметрах товара, т.е. запихиваем выбранный товар в exists
      const exists = state.cart.items.filter(i => i.product.id === item.product.id)

      // если в exists что-то есть, 
      if(exists.length){
        exists[0].quantity = parseInt(exists[0].quantity) + parseInt(item.quantity)
      }
      else{
        state.cart.items.push(item)
      }

      localStorage.setItem('cart', JSON.stringify(state.cart))
    },
    setIsLoading(state, status){
      state.isLoading = status
    },
    //при успешной авторизции
    setToken(state, token){
      state.token = token
      state.isAuthentificated = true
    },
    //если пользователь разлогинился
    removeToken(state){
      state.token = ''
      state.username = ''
      state.isAuthentificated = false
    },
    clearCart(state){
      state.cart = { items: [] }
      // в локал сторадж заполняем пустую корзину
      localStorage.setItem('cart', JSON.stringify(state.cart))
    }
  },
  actions: {
  },
  modules: {
  }
})
