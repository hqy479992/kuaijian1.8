//全局变量

window.onload=function(){
	var obj={
		'resultfiles':'resultfiles'
	}
	$.ajax({
		url:'resultfiles',
		type:'POST',
		data:JSON.stringify(obj),
		async:true,
		success:function(data){
			if (data=='error') {
				// do nothing
			}
			else{
				showdirs(data)
			}
		}
	})
}

//click事件
var chosed=function(buttonobj){
	if(buttonobj.innerHTML.lastIndexOf('fa-square-o')!=-1){
		$(buttonobj).html(buttonobj.innerHTML.replace('fa-square-o','fa-check-square-o'))
		$('#download').attr('href','/downloadbigfile?filename='+findfirstchosed().text())
	}
	else{
		$(buttonobj).html(buttonobj.innerHTML.replace('fa-check-square-o','fa-square-o'))
	}
}

$('#suredelete').click(function(){
	if(findfirstchosed().text()==''){
		//do nothing
	}
	else{
		var folderin=findfirstchosed().text().lastIndexOf('/')
		var obj
		if (folderin==-1) {
			obj={
				'path':'static/resultfiles',
				'deletefilename':findfirstchosed().text(),
				'nowfolder':''
			}
		}
		else{
			obj={
				'path':'static/resultfiles',
				'deletefilename':findfirstchosed().text(),
				'nowfolder':findfirstchosed().text().slice(0,folderin)+'/'
			}
		}
		$.ajax({
			url:'deletefile',
			type:'POST',
			data:JSON.stringify(obj),
			async:true,
			success:function(data){
				if(data=='error'){
					//do nothing
				}
				else{
					$('#deletefilemodal').modal('hide')
					showdirs(data)
				}
			}
		})
	}
})

//show事件
$('#deletefilemodal').on('show.bs.modal',function(event){
	if (findfirstchosed().text()=='') {
		$('#deletefilename').append('未选择文件！')
	}
	else{
		$('#deletefilename').append('将要删除 '+findfirstchosed().text()+' ！删除后将不可恢复！')
	}
})

//其他函数
function showdirs(data){
	$('#showboard').html('')
	data=JSON.parse(data)
	for (path in data) {
		if(data[path]=='dir'){
			$('#showboard').append($('<button>').attr('type','button').attr('class','btn btn-outline-info ml-3 border-0').attr('onclick','chosed(this)').append(
									$('<span>').attr('class','fa fa-square-o fa-lg mr-5 pr-5'),
									$('<br>'),
									$('<span>').attr('class','fa fa-folder fa-5x'),
									$('<br>'),
									$('<p>').append(path)))
		}
		else if(data[path]=='.mp3'){
			$('#showboard').append($('<button>').attr('type','button').attr('class','btn btn-outline-info ml-3 border-0').attr('onclick','chosed(this)').append(
									$('<span>').attr('class','fa fa-square-o fa-lg mr-5 pr-5'),
									$('<br>'),
									$('<span>').attr('class','fa-stack fa-2x my-2').append(
										$('<i>').attr('class','fa fa-file-o fa-stack-2x'),
										$('<i>').attr('class','fa fa-music fa-stack-1x')),
									$('<br>'),
									$('<p>').append(path)))
		}
		else if(data[path]=='.mp4'){
			$('#showboard').append($('<button>').attr('type','button').attr('class','btn btn-outline-info ml-3 border-0').attr('onclick','chosed(this)').append(
									$('<span>').attr('class','fa fa-square-o fa-lg mr-5 pr-5'),
									$('<br>'),
									$('<img>').attr('src','static/resultfiles/'+path.slice(0,-4)+'mvtojpg.jpg').attr('class','showmvimg'),
									$('<p>').append(path)))
		}
		else if(data[path]=='.xml'){
			$('#showboard').append($('<button>').attr('type','button').attr('class','btn btn-outline-info ml-3 border-0').attr('onclick','chosed(this)').append(
									$('<span>').attr('class','fa fa-square-o fa-lg mr-5 pr-5'),
									$('<br>'),
									$('<span>').attr('class','fa fa-file-code-o fa-4x my-2'),
									$('<br>'),
									$('<p>').append(path)))
		}
		else if (data[path]=='.jpg') {
			if(path.substr(-11)=='mvtojpg.jpg'){
				//do nothing
			}
			else{
				$('#showboard').append($('<button>').attr('type','button').attr('class','btn btn-outline-info ml-3 border-0').attr('onclick','chosed(this)').append(
										$('<span>').attr('class','fa fa-square-o fa-lg mr-5 pr-5'),
										$('<br>'),
										$('<img>').attr('src','static/uploadfiles/'+path+'.jpg').attr('class','showmvimg'),
										$('<p>').append(path)))
			}
		}
		else{
			$('#showboard').append($('<button>').attr('type','button').attr('class','btn btn-outline-info ml-3 border-0').attr('onclick','chosed(this)').append(
									$('<span>').attr('class','fa fa-square-o fa-lg mr-5 pr-5'),
									$('<br>'),
									$('<span>').attr('class','fa fa-file-o fa-4x my-2'),
									$('<br>'),
									$('<p>').append(path)))
		}
	}
}

function findfirstchosed(){
	return $('#showboard').children('button').children('span.fa-check-square-o').siblings('p')
}