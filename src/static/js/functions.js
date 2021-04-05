
function changePageHeaderForUser()
{
  document.getElementById("right_top_header_section").innerHTML=
/*  '     <a href="/manage-images">'+
  '      <button type="button" '+
  '         class="btn btn-success mb-0 mr-2"'+
  '          style="font-weight: bold;font-size: 150%;">'+
  '            My Images'+
  '      </button>'+
  '     </a>'+*/
  '     <a href="/manage-products">'+
  '      <button type="button" '+
  '         class="btn btn-success mb-0 mr-2"'+
  '          style="font-weight: bold;font-size: 150%;">'+
  '            My Products'+
  '      </button>'+
  '     </a>'+

  '     <a href="/cart">'+
  '      <button type="button" '+
  '         class="btn btn-success mb-0 mr-2"'+
  '          style="font-weight: bold;font-size: 150%;">'+
  '            My Cart'+
  '      </button>'+
  '     </a>'+
  '      <button type="button" '+
  '         class="btn btn-outline-danger mb-0 mr-2"'+
  '          style="font-weight: bold;font-size: 150%;"'+
  '          onclick="signTheUserOut()">'+
  '            Sign Out'+
  '      </button>';
}


function changeHeaderIfYouSHould()
{
  who().then(function(data, textStatus, xhr) {
        if (xhr.status==200) {changePageHeaderForUser()}});
}

function signTheUserOut()
{
  logout_users().then(
    function(response){
    window.location.href="/";}
    );
}

changeHeaderIfYouSHould();







