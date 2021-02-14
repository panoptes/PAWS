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
  updateAladin()
}

function updateAladin() {
  results={};
  jQuery.get('http://localhost:8000/static/images/HIPS/properties', function(data) {
    parts=data.split("\n");
    for (var i=0;i<parts.length;i++){
      var nameAndValue=parts[i].split("=")
      if(nameAndValue.length==2) {
	    results[ $.trim(nameAndValue[0]) ] = $.trim(nameAndValue[1])
	  }
    }

    dec = parseFloat(results["hips_initial_dec"].match(/-?(?:\d+(?:\.\d*)?|\.\d+)/)[0])
    ra = parseFloat(results["hips_initial_ra"].match(/-?(?:\d+(?:\.\d*)?|\.\d+)/)[0])
    fov = parseFloat(results["hips_initial_fov"].match(/-?(?:\d+(?:\.\d*)?|\.\d+)/)[0])

    // Update position
    Aladin.aladin.gotoRaDec(ra, dec)
    Aladin.aladin.setFov(fov)
  });
}

$( document ).keyup(function(e) {
  if (String.fromCharCode(e.which).toLocaleLowerCase() == "t") {
    if (Aladin.aladin != null) {
      if (Aladin.aladin.getBaseImageLayer().id == Aladin.my_fits_bil_id) {
        Aladin.aladin.setBaseImageLayer(Aladin.reference_bil_id)
      } else {
        Aladin.reference_bil_id = Aladin.aladin.getBaseImageLayer().id;
        Aladin.aladin.setBaseImageLayer(Aladin.my_fits_bil_id)
      }
    }
  }
});
