document.addEventListener("DOMContentLoaded", function () {
    console.log("Admin panel loaded!");
    console.log("Dropdown menu loaded!");

    // Reload page after clicking any link
    document.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", function () {
            setTimeout(() => location.reload(), 500);
        });
    });

   
    $(document).ready(function () {
        // Ensure jQuery is loaded before running Owl Carousel
        if (typeof jQuery !== "undefined") {
            if ($(".best-sellers-carousel").length) { // Check if carousel exists
                $(".best-sellers-carousel").owlCarousel({
                    loop: true,
                    margin: 10,
                    nav: true,  // Enables left/right arrows
                    dots: false, // Removes bottom dots
                    autoplay: true,
                    autoplayTimeout: 3000,
                    responsive: {
                        0: { items: 1 },
                        600: { items: 3 },
                        1000: { items: 5 }
                    }
                });
    
                // Force refresh to ensure navigation is visible
                $(".best-sellers-carousel").trigger('refresh.owl.carousel');
            } else {
                console.warn("No element with class 'best-sellers-carousel' found.");
            }
        } else {
            console.error("jQuery is not loaded. Make sure to include jQuery before this script.");
        }
    });

    document.addEventListener("DOMContentLoaded", function() {
        document.querySelectorAll(".dropdown-menu").forEach(menu => {
            menu.addEventListener("click", function(event) {
                event.stopPropagation(); // Prevent dropdown from closing when clicking inside
            });
        });
    });
    
    document.getElementById("searchForm").addEventListener("submit", function() {
        document.getElementById("searchResults").innerHTML = ""; // Clears search results before showing new ones
    }); 



});
