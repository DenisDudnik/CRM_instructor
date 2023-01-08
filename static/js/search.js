"use strict";
window.addEventListener('load', () => {
   const search = document.querySelector('#search');
   const body = document.querySelector('.cards-container');
   const rows = body.querySelectorAll('.card');
   console.dir(rows);
   search.addEventListener('input', event => {
       const value = event.target.value.toLowerCase();
       if (value === '') {
           rows.forEach(el => {
               el.style.display = '';
           })
       } else {
           rows.forEach(el => {
               let val = el.querySelector('a.name').innerText.toLowerCase();
               if (val.includes(value)) {
                   el.style.display = '';
               } else {
                   el.style.display = 'none';
               }
           })
       }
   })
});
