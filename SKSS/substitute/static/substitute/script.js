document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.need-check').forEach(element =>{
        element.onsubmit = function() {
            if(window.confirm('送信しても良いですか？')) {
                return true;
              } else {
                return false;
            }
        };
    })
})