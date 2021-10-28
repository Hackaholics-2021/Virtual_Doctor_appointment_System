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

// faq dropdown in desktop
var dropdown_question = document.getElementsByClassName("question");
for(var j=0;j<dropdown_question.length;j++){
    dropdown_question[j].addEventListener("click", function(){
        var dropdownContent = this.nextElementSibling;

        if(dropdownContent.style.display=="flex"){
            dropdownContent.style.display="none";
            var image = this.children[0];
            image.setAttribute("src","../static/images/right-arrow.png");
        }
        else{
            dropdownContent.style.display="flex";
            var image = this.children[0];
            image.setAttribute("src","../static/images/arrow-down.png");
        }
    });
}
