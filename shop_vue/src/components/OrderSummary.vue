<template>
    <div class="box mb-4">
        <!-- номер ордера -->
        <h3 class="is-size-4 mb-6">Order №{{ order.id }}</h3>

        <h4 class="is-size-5">Products</h4>

        <table class="table is-fullwidth">
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Total</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="item in order.items" 
                v-bind:key="item.product.id">
                    <td>{{ item.product.name }}</td>
                    <td>${{ item.product.price }}</td>
                    <td>{{ item.quantity }}</td>
                    <td>{{ getItemTotal(item).toFixed(2) }}</td>
                </tr>
                
                <tr>
                    <td colspan="2"><strong>Total</strong></td>
                    <td>{{getItemTotalQuantity(order)}}</td>
                    <td>${{ getItemTotalPrice(order).toFixed(2) }}</td>
                    <!-- <td>{{order.paid_amount}}</td> -->
                </tr>
            </tbody>

        </table>
    </div>
</template>

<script>
export default {
  name: "OrderSummary",
  data(){
      return{
          total: 0,

      }
  },
  props: {
      order: Object
  },
  mounted(){

  },
  methods: {
      getItemTotal(item){
          return item.quantity * item.product.price
      },
      orderTotalLength(order){
          return order.items.reduce((acc, curVal) =>{
              total += curVal.quantity
              return acc += curVal.quantity
          }, 0)
      },
      getItemTotalQuantity(order){
          return order.items.reduce((acc,item) =>{
              return acc += item.quantity
          }, 0)
      },
      getItemTotalPrice(order){
          return order.items.reduce((acc, item) => {
              return acc += item.product.price * item.quantity
          }, 0)
      }
  }
};
</script>
