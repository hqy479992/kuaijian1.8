//全局变量
var task_name='',
	head_duration=10,
	tail_duration=10,
	window_size=[0,125],
	min_output_duration=[10],
	max_output_duration=[20]

window.onload=function(){
	for (var i = 0; i < getParams('chanelsum'); i++) {
		min_output_duration[i]=10
		max_output_duration[i]=20
		if (i==0) 
		{
			window_size[i]=0
		}
		else
		{
			window_size[i]=125
		}
	}
	$('.headduration').attr('value',head_duration)
	$('.tailduration').attr('value',tail_duration)
	for (var i = 0; i < getParams('chanelsum'); i++) {
		if (i==0) {
			$('.windowsize').children('div.input-group-append').prev().attr('value',window_size[i])
			$('.minoutputduration').children('div.input-group-append').prev().attr('value',min_output_duration[i])
			$('.maxoutputduration').children('div.input-group-append').prev().attr('value',max_output_duration[i])
		}
		else{
			$('.windowsize').children('div.input-group-append').before('<input type="text" class="form-control" value="'+window_size[i].toString()+'">')
			$('.minoutputduration').children('div.input-group-append').before('<input type"text" class="form-control" value="'+min_output_duration[i].toString()+'">')
			$('.maxoutputduration').children('div.input-group-append').before('<input type="text" class="form-control" value="'+max_output_duration[i].toString()+'">')
		}
	}
}

//click事件
$('#startsyn').click(function(){
	task_name=$($('div.col-10 input')[0]).val()
	if (task_name=='') {
		//必须填写！
		alert('error')
	}
	head_duration=$($('div.col-10 input')[1]).val()
	tail_duration=$($('div.col-10 input')[2]).val()
	var j=0,k=0,n=0
	for (var i = 3; i < $('div.col-10 input').length; i++) {
		if (i<3+($('div.col-10 input').length-3)/3) {
			window_size[j]=$($('div.col-10 input')[i]).val()
			j++
		}
		else if (i<3+($('div.col-10 input').length-3)*2/3) {
			min_output_duration[k]=$($('div.col-10 input')[i]).val()
			k++
		}
		else{
			max_output_duration[n]=$($('div.col-10 input')[i]).val()
			n++
		}
	}
	var obj={
		'task_name':task_name,
		'window_size':window_size,
		'min_output_duration':min_output_duration,
		'max_output_duration':max_output_duration,
		'head_duration':head_duration,
		'tail_duration':tail_duration,
	}
	$.ajax({
		url:'/settingsvalue',
		type:'POST',
		data:JSON.stringify(obj),
		async:true,
		success:function(data){
			if (data=='success') {
				window.location.href='/doing'
			}
			else{
				//do nothing
			}
		}
	})
})

//其他函数
function getParams(key){
	var reg=new RegExp('(^|&)'+key+'=([^&]*)(&|$)')
	var r=window.location.search.substr(1).match(reg)
	if (r!=null) {
		return decodeURI(r[2])
	}
	return null
}