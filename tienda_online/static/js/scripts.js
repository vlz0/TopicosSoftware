/*!
* Start Bootstrap - Shop Item v5.0.6 (https://startbootstrap.com/template/shop-item)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-item/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project 

// add to cart 
$(".add-to-cart-btn").on("click",function(){  
    let quantity = $("#product-quantity").val() 
    let product_title=$("#product-title").val() 
    let product_id=$(".product-id").val() 
    let product_price=$("current-product-price").text()  
    let this_val=$(this)


    console.log("Quantity: ",quantity); 
    console.log("Title: ", product_title);  
    console.log("Price: ", product_price); 
    console.log("Current element: ", this_val); 




})