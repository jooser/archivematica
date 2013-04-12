<script type="text/javascript">

function AddElement(){  
        var theNewElem = document.createElement('input');  
        theNewElem.setAttribute('type','submit');  
        theNewElem.setAttribute('value','continue');  
        document.getElementById('FormHere').appendChild(theNewElem);   
      }  
      
function moreStuff() {
    $("div#fpr").append("<p>Updating format policy rules . . .</p>");
    $.get("installer/fprdownload/", function(data, textStatus)
    {
        if (data['result'] == 'success') {
            $("div#fpr").append("<p>" + data['response'] + "</p>");
            AddElement();
        } else {
            $("div#fpr").append("<p>Unable to update FPR.</p>");
            AddElement(); 
        }
    }, "json");
}

</script>