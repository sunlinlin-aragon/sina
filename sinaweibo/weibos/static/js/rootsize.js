Rem();
function Rem() {
    var docEl = document.documentElement,
    oSize = docEl.clientWidth / 7.5;

    docEl.style.fontSize = oSize + 'px';
}

window.addEventListener('resize', Rem, false);