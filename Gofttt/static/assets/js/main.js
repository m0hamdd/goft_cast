(function ($) {
    "use strict";
    $(window).on('load', function () {
        $(".preloader").fadeOut("slow");
    });
    $('.dropdown-menu a.dropdown-toggle').on('click', function (e) {
        if (!$(this).next().hasClass('show')) {
            $(this).parents('.dropdown-menu').first().find('.show').removeClass('show');
        }
        var $subMenu = $(this).next('.dropdown-menu');
        $subMenu.toggleClass('show');
        $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function (e) {
            $('.dropdown-submenu .show').removeClass('show');
        });
        return false;
    });
    if ($('.search-box-outer').length) {
        $('.search-box-outer').on('click', function () {
            $('body').addClass('search-active');
        });
        $('.close-search').on('click', function () {
            $('body').removeClass('search-active');
        });
    }
    $(document).on('ready', function () {
        $("[data-background]").each(function () {
            $(this).css("background-image", "url(" + $(this).attr("data-background") + ")");
        });
    });
    $('.sidebar-btn').on('click', function () {
        $('.sidebar-popup').addClass('open');
        $('.sidebar-wrapper').addClass('open');
    });
    $('.close-sidebar-popup, .sidebar-popup').on('click', function () {
        $('.sidebar-popup').removeClass('open');
        $('.sidebar-wrapper').removeClass('open');
    });
    new WOW().init();
    $('.hero-slider').owlCarousel({
        loop: true,
        nav: true,
        dots: true,
        margin: 0,
        autoplay: true,
        autoplayHoverPause: true,
        autoplayTimeout: 5000,
        items: 1,
        navText: ["<i class='fal fa-angle-left'></i>", "<i class='fal fa-angle-right'></i>"],
        onInitialized: function (event) {
            var $firstAnimatingElements = $('.owl-item').eq(event.item.index).find("[data-animation]");
            doAnimations($firstAnimatingElements);
        },
        onChanged: function (event) {
            var $firstAnimatingElements = $('.owl-item').eq(event.item.index).find("[data-animation]");
            doAnimations($firstAnimatingElements);
        }
    });

    function doAnimations(elements) {
        var animationEndEvents = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
        elements.each(function () {
            var $this = $(this);
            var $animationDelay = $this.data('delay');
            var $animationDuration = $this.data('duration');
            var $animationType = 'animated ' + $this.data('animation');
            $this.css({
                'animation-delay': $animationDelay,
                '-webkit-animation-delay': $animationDelay,
                'animation-duration': $animationDuration,
                '-webkit-animation-duration': $animationDuration,
            });
            $this.addClass($animationType).one(animationEndEvents, function () {
                $this.removeClass($animationType);
            });
        });
    }
    $('.show-slider').owlCarousel({
        loop: true,
        margin: 24,
        nav: true,
        dots: true,
        autoplay: false,
        navText: ["<i class='far fa-angle-left'></i>", "<i class='far fa-angle-right'></i>"],
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 2
            },
            1400: {
                items: 4
            }
        }
    });
    $('.testimonial-slider').owlCarousel({
        loop: true,
        margin: 10,
        nav: false,
        dots: true,
        autoplay: false,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 2
            },
            1400: {
                items: 3
            }
        }
    });
    $('.instagram-slider').owlCarousel({
        loop: true,
        margin: 0,
        nav: false,
        dots: false,
        autoplay: true,
        responsive: {
            0: {
                items: 2
            },
            600: {
                items: 3
            },
            1000: {
                items: 6
            }
        }
    });
    $('.partner-slider').owlCarousel({
        loop: true,
        margin: 30,
        nav: false,
        dots: false,
        autoplay: true,
        responsive: {
            0: {
                items: 2
            },
            600: {
                items: 3
            },
            1000: {
                items: 6
            }
        }
    });
    $('.counter').countTo();
    $('.counter-box').appear(function () {
        $('.counter').countTo();
    }, {
        accY: -100
    });
    $(".popup-gallery").magnificPopup({
        delegate: '.popup-img',
        type: 'image',
        gallery: {
            enabled: true
        },
    });
    $(".popup-youtube, .popup-vimeo, .popup-gmaps").magnificPopup({
        type: "iframe",
        mainClass: "mfp-fade",
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false
    });
    $(window).scroll(function () {
        if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
            $(".scroll-top").addClass('active');
        } else {
            $(".scroll-top").removeClass('active');
        }
    });
    $(".scroll-top").on('click', function () {
        $("html, body").animate({
            scrollTop: 0
        }, 1500);
        return false;
    });

    function scrollProgress() {
        const scrollProgressbar = document.querySelector('.scroll-progress-bar');
        if (scrollProgressbar) {
            const scrollTotalHeight = document.body.scrollHeight - window.innerHeight;
            let scrollProgress = (window.scrollY / scrollTotalHeight) * 283;
            scrollProgress = Math.min(scrollProgress, 283);
            scrollProgressbar.style.strokeDashoffset = 283 - scrollProgress;
        }
    }
    scrollProgress();
    window.addEventListener('scroll', scrollProgress);
    window.addEventListener('resize', scrollProgress);
    $(window).scroll(function () {
        if ($(this).scrollTop() > 50) {
            $('.navbar').addClass("fixed-top");
        } else {
            $('.navbar').removeClass("fixed-top");
        }
    });
    $(window).on('load', function () {
        if ($(".filter-box").children().length > 0) {
            $(".filter-box").isotope({
                itemSelector: '.filter-item',
                masonry: {
                    columnWidth: 2
                },
            });
            $('.filter-btn').on('click', 'li', function () {
                var filterValue = $(this).attr('data-filter');
                $(".filter-box").isotope({
                    filter: filterValue
                });
            });
            $(".filter-btn li").each(function () {
                $(this).on("click", function () {
                    $(this).siblings("li.active").removeClass("active");
                    $(this).addClass("active");
                });
            });
        }
    });
    $('[data-countdown]').each(function () {
        let finalDate = $(this).data('countdown');
        $(this).countdown(finalDate, function (event) {
            $(this).html(event.strftime('<div class="time-wrap">' + '<span class="time"><span>%-D</span><span class="unit">روز</span></span>' + ' <span class="divider">:</span> ' + '<span class="time"><span>%H</span><span class="unit">ساعت </span></span>' + ' <span class="divider">:</span> ' + '<span class="time"><span>%M</span><span class="unit">دقیقه</span></span>' + ' <span class="divider">:</span> ' + '<span class="time"><span>%S</span><span class="unit">ثانیه</span></span>' + '</div>'));
        });
    });
    if ($('.select').length) {
        $('.select').niceSelect();
    }
    let date = new Date().getFullYear();
    $("#date").html(date);
})(jQuery);