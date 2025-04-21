document.addEventListener('DOMContentLoaded', function() {
    // Get the modal
    var modal = document.querySelector(".modal");

    // Get all divs that open the modal
    var divs = document.querySelectorAll(".openPopupDiv");

    // Get the <span> element that closes the modal
    var span = document.querySelector(".close");

    // When any div is clicked, open the modal
    divs.forEach(function(div) {
        div.addEventListener('click', function() {
            modal.style.display = "block";
        });
    });

    // When the user clicks on <span> (x), close the modal
    span.addEventListener('click', function() {
        modal.style.display = "none";
    });

    // When the user clicks anywhere outside of the modal, close it
    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
      // When the user clicks on submit button, close the modal
    // submitBtn.onclick = function() {
    //     modal.style.display = "none";
    // }
});


