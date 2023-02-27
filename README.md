# Online-Shop-RESTApi

## This is the RESTApi server created for the https://github.com/tonnyhc/Online-Shop-React-Client (Online sunglasses shop)

## Getting started

    The server is using PostgreSQL. If you want to use another one you can set it up in settings.py
    To start the server you must install all the requirements using pip install requirements.txt.

## Views docs

    - Products
        on path /api/products you can see the list of all the products in the DB
        on path /api/products/<product_slug>/rate you can give a rating for the product. The server is expecting a body in the following format
            {
                "score": "{0 to 5 delimiter 0.5}"
            }

    - Basket
        on path /api/basket/<str:username> you can see the logged in user's basket and all its items
        on path /api/basket/add-to-basket/<product:slug> you can add a product to the user's basket. Expected data:
            {
                "product": <product_slug>,
                "quantity": (default is 1),
            }
        on path /api/basket/remove-from-basket/<product:slug> you can remove item from the user's basket. Expected data:


            This view expects a 'DELETE' method with body
            {
                'product': <product_slug>
            }
            and must include the user token
            and the csrf_token
            in the Headers
    
    - Orders
        on path /api/orders/create you can create an order. The server is expecting following data:
            {
                full_name,
                phone_number,
                town,
                address,
                post_code
                items: [
                    {
                        slug: slug1
                    },
                    {
                        slug: slug2
                    }
                ]
            }
