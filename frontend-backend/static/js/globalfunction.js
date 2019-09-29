//显示bootstrap4提示框效果
$('[data-toggle="tooltip"]').tooltip()

//显示上方navbar(header)
$('#header').load('header')

//显示侧方navbar
$('nav.col-2').load('navbar')

//两个html之间通过url传递信息时，使用getParams('param1')即可从/example.html?param1='param1value'中获取'param1'的值param1value
function getParams(key){
	var reg=new RegExp('(^|&)'+key+'=([^&]*)(&|$)')
	var r=window.location.search.substr(1).match(reg)
	if (r!=null) {
		return decodeURI(r[2])
	}
	return null
}