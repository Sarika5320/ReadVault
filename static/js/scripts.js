document.addEventListener("DOMContentLoaded", function() {
  console.log("Admin panel loaded!");
});
document.addEventListener("DOMContentLoaded", function() {
  console.log("Dropdown menu loaded!");
});



document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", function() {
            setTimeout(() => location.reload(), 500); // Reload page after 500ms
        });
    });
});


