function onAladinLoadHandler() {
  // Init stuff
  Aladin.aladin = document.getElementById("aladin_iframe_id").contentWindow.aladin;
  Aladin.my_fits_bil_id = Aladin.aladin.getBaseImageLayer().id;
  Aladin.reference_bil_id = "DSS color";

  // Initialize nice looking options
  Aladin.aladin.toggleFullscreen(Aladin.aladin.options.realFullscreen);
  // Debug stuff to be removed
  //var aladin_bil = aladin.getBaseImageLayer();
  //var aladin_initial_color_map = aladin_bil.getColorMap();
  //aladin_initial_color_map.update("rainbow");
}

$( document ).keyup(function(e) {
  console.log("KEY IS PRESSED "+String.fromCharCode(e.which));
  if (String.fromCharCode(e.which).toLocaleLowerCase() == "t") {
    if (Aladin.aladin != null) {
      if (Aladin.aladin.getBaseImageLayer().id == Aladin.my_fits_bil_id) {
        Aladin.aladin.setBaseImageLayer(Aladin.reference_bil_id)
      } else {
        Aladin.aladin.setBaseImageLayer(Aladin.my_fits_bil_id)
      }
    }
  }
});
