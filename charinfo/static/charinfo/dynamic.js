$(document).ready(function () {
  updateTiles();
});

function updateTiles() {
  $("div.tile").each(function (index) {
    var characterID = $(this).data("charid");
    $(this).load("/evedashboard/charinfo/tile/" + characterID + "/");
  });

  setTimeout(updateTiles, 30000);
}
