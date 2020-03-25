
//WINDOW.ONLOAD IS CALLED AFTER THE HTML FILE IS LOADED
window.onload = function(){
  var text = "This text was made using Javascript"

  //THIS GETS THE ELEMENT OF THE DOCUMENT BY ID AND MODIFIES THE HTML INSIDE
  document.getElementById("first_paragraph").innerHTML = text;
};

//TO USE DATA FROM THE SERVER WE WOULD MAKE A REQUEST AND THEN USE THE ABOVE METHOD TO MODIFY THE HTML
