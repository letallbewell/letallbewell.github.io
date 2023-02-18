function open_tab(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  }
  
// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();

function change_link_targets() {

  var links = document.links;
  for (var i = 0; i < links.length; i++) {
      if (!(links[i].href.includes('github.io'))) {
          links[i].target = "_blank";
      }
  }
  document.links = links;
}

