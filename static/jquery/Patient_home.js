var counters = document.querySelectorAll(".customer-title");
var speed=400;
$(window).scroll(function() {
    var hT = $('.customers').offset().top,
        hH = $('.customers').outerHeight(),
        wH = $(window).height(),
        wS = $(this).scrollTop();
    if (wS > (hT+hH-wH)){
        counters.forEach(counter => {
            const updateCount = () =>{
                const target=+counter.getAttribute("data-target");
                const present = +counter.innerText;
                const inc=target/speed;
                if(present<target){
                    counter.innerText = Math.ceil(present+inc);
                    setTimeout(updateCount,1);
                }
                else{
                    counter.innerText=target.toString();
                    counter.innerText+="+";
                }
            }
            updateCount();
            
        });
    }
});
