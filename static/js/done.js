//全局变量
'use strict'

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
	var path
	for (path in data) {
		var diffrenticon=``
		var basicbuttonbefore=`<button type="button" class="btn btn-outline-info ml-3 border-0" onclick="chosed(this)">
							<span class="fa fa-square-o fa-lg mr-5 pr-5"></span>
							<br>`
		var basicbuttonafter=`<br>
							<p>${path}</p>
						</button>`
		
		if(data[path].toLowerCase()=='dir'){
			diffrenticon=`<span class="fa fa-folder fa-5x"></span>`
			$('#showboard').append(basicbuttonbefore+diffrenticon+basicbuttonafter)
		}
		else if(data[path].toLowerCase()=='.mp3'){
			diffrenticon=`<span class="fa-stack fa-2x my-2">
								<i class="fa fa-file-o fa-stack-2x"></i>
								<i class="fa fa-music fa-stack-1x"></i>
							</span>`
			$('#showboard').append(basicbuttonbefore+diffrenticon+basicbuttonafter)
		}
		else if(data[path].toLowerCase()=='.mp4'){
			var videoname=path.slice(0,-4)
			diffrenticon=`<img src="static/resultfiles/${videoname}mvtojpg.jpg" class="showmvimg">`
			$('#showboard').append(basicbuttonbefore+diffrenticon+basicbuttonafter)
		}
		else if(data[path].toLowerCase()=='.xml'){
			diffrenticon=`<span class="fa fa-file-code-o fa-4x my-2"></span>`
			$('#showboard').append(basicbuttonbefore+diffrenticon+basicbuttonafter)
		}
		else if (data[path].toLowerCase()=='.jpg') {
			if(path.substr(-11)=='mvtojpg.jpg'){
				//do nothing
			}
			else{
				diffrenticon=`<img src="static/resultfiles/${path}" class="showmvimg">`
				$('#showboard').append(basicbuttonbefore+diffrenticon+basicbuttonafter)
			}
		}
		else{
			if (path=='kuaijianresultfilestest.txt') {
				//do nothing
			}
			else{
				diffrenticon=`<span class="fa fa-file-o fa-4x my-2"></span>`
				$('#showboard').append(basicbuttonbefore+diffrenticon+basicbuttonafter)
			}
		}
	}
}

function findfirstchosed(){
	return $('#showboard').children('button').children('span.fa-check-square-o').siblings('p')
}