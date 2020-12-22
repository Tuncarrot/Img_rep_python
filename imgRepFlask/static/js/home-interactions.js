function switchLayout() {
    var icon = document.getElementById("layout-icon");
    var para = document.getElementById("layout-paragraph");
    if (icon.style.display === "none") {
        icon.style.display = "block";
        para.style.display = "none";
    } else {
        icon.style.display = "none";
        para.style.display = "block";
    }
  } 

