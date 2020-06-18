# Backend Routes

1. Users:
   - POST "/users"
     -  endpoint will create a new user
   - PUT "/users/:user_id"
     -  endpoint will update user information


2. Charities:
    - GET "/"
        - endpoint returns home page with featured charities
    - POST@requires_auth "/charity/:user_id"
        - endpoint saves a new charity donated to for a user
    - PUT@requires_auth "/charity/:user_id"
        - endpoint updates a users portfolio of charity donated to
    - DELETE@requires_auth "/charity/:user_id"
        - endpoint deletes a charity donated to 


3. Portfolio:
    - GET@requires_auth "/:user_id/portfolio"
        - endpoint returns an overview of a users portfolio
    - DELETE@requires_auth "/:user_id/portfolio"
        - endpoint deletes charities from the portfolio


 4. Favorites:
   - POST@requires_auth "/:charity_id/favorite"
     - This endpoint adds a favorite to charity @id for logged in user
   - DELETE@requires_auth "/charity:id/favorite/delete
     - This endpoint removes a favorite to charity @id for logged in user
    
