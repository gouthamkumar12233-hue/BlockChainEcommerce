pragma solidity >= 0.8.11 <= 0.8.11;

contract Ecommerce {
    string public user_signup;
    string public add_product;
    string public book_order;
    
    //add signup details details	
    function addUser(string memory us) public {
       user_signup = us;	
    }
   //get user details
    function getUser() public view returns (string memory) {
        return user_signup;
    }

    function addProduct(string memory ad) public {
       add_product = ad;	
    }

    function getProduct() public view returns (string memory) {
        return add_product;
    }

    function bookOrder(string memory bo) public {
      book_order = bo;	
    }

    function getOrder() public view returns (string memory) {
        return book_order;
    }

    constructor() public {
        user_signup = "";
	add_product="";
	book_order="";
    }
}