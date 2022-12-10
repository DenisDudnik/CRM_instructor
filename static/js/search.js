"use strict";
window.addEventListener('load', () => {
   const search = document.querySelector('#search');
   const body = document.querySelector('TBODY');
   const rows = body.querySelectorAll('TR');
   console.dir(rows);
   search.addEventListener('input', event => {
       const value = event.target.value.toLowerCase();
       if (value === '') {
           rows.forEach(el => {
               el.style.display = '';
           })
       } else {
           rows.forEach(el => {
               let val = el.querySelector('TD:nth-child(2)').querySelector('A').innerText.toLowerCase();
               if (val.includes(value)) {
                   el.style.display = '';
               } else {
                   el.style.display = 'none';
               }
           })
       }
   })
});
