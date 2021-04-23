    // DB에서 food 받아오기
    function get_food() {
      $.ajax({
        type: "GET",
        url: '/result',
        data: {},
        success: function (response) {
          let foods = response["foods"]
          // 난수 생성 후 랜덤 음식점 가져오기
          let random = Math.floor(Math.random() * 10);
          let food = foods[random]
          // 음식 결과 출력 함수 호출
          food_info(food)
        }
      }
      );
    }

    // function food_list(foods) {
    //   for (let i = 0; i < foods.length; i++) {
    //     let food_list_title = foods[i]['title'];
    //     let food_list_category = foods[i]['category'];
    //     let food_list_a_href = foods[i]['a_href'];
    //     let food_address = foods[i]['address'];
    //     let food_list_img_src = foods[i]['img_src'];
    //     let food_address_select = food_address.substring(0, 2);
    //     if (food_address_select === "서울") {
    //       console.log(food_address)
    //       let html_temp = `    <div class="rows">
    //                              <a href="${food_list_a_href}" class="food_list_a" target="_blank">
    //                             <div class="col">
    //                               <img src="${food_list_img_src}" class="food_list_pic">
    //                             </div>

    //                               <div class="col_text"> <span class="food_list_title">${food_list_title}</span>
    //                                 <span class="food_list_category">${food_list_category}</span> <span class=food_list_address>${food_address}</span>
    //                               </div>
    //                             </a>
    //                           </div>`
    //       $(".food_list").append(html_temp);
    //     }

    //   }
    // }

    // food에서 각 정보 넣고 좌표 변환 함수에 좌표 보내기
    function food_info(food) {
      console.log(food)
      let address = food['address'];
      let category = food['category'];
      let img_src = food['img_src'];
      let title = food['title'];
      let tel = food['tel'];
      let a_href = food['a_href'];
      $('#food-address').text(address);
      $('#food-category').text(category);
      $('#food-title').text(title);
      $('#food-image').attr("src", img_src);
      $('#food-tel').text(tel);
      $('#food-atag').attr("href", a_href);
    }


    // function getPagination(page, size) {
    //   $.ajax({
    //     type: 'GET',
    //     url: '/resultpage',
    //     data: {
    //       'page': page,
    //       'size': size,
    //     },
    //     success: function (res){
    //       if (res['result'] === 'success'){
    //         let data = res['data']
    //         let total = res['total']
    //         drawPagination(total, page, size)
    //       }
    //     }
    //   })
    // }

    // // 페이지네이션 그리기 함수
    // function drawPagination(total, page, size) {
    //   // 11개 데이터가 있을 때, size가 10이면 2page가 나와야하므로 올림
    //   let totalPage = Math.ceil(tota / size)
    //   console.log('total :', total, 'size :', size, 'totalPage :', totalPage)
    // }
    // let page = 1
    // let size = 9
    
    $(documnet).ready(function() {
      get_food()
      // getPagination(page, size)
    })
