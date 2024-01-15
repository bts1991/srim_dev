var xmlPath = '/static/companylist.txt';
var results = [];
var datagb = '0'; //0:모두, 1:Company만, 3:EFT만
LoadData();

$(document).ready(function() {
	$("#SearchText").autocomplete({
		data: results,
		matchContains: true,
		minChars: 0,
		width: 150,
		delay: 10,
		sortResults: true,
		sortFunction : sortFunction,
		showResult : showResult,
		onItemSelect: selectResult,
		formatItem : formatItem,
		displayValue : displayValue,
		highlightItem: false,
		maxItemsToShow: 20
	});
	//$("#SearchText").focus();
});
sortFunction = function(a, b, filter) {
	a = String(a.value);
	b = String(b.value);
	a = a.toLowerCase();
	b = b.toLowerCase();
	var indexA = a.indexOf(filter,0);
	var indexB = b.indexOf(filter,0);
	if (indexA==indexB)
	{
		if (a > b) {
			return 1;
		}
		if (a < b) {
			return -1;
		}
	} else {
		if (indexA > indexB) {
			return 1;
		}
		if (indexA < indexB) {
			return -1;
		}

	}
	return 0;
};
function LoadData() {
	$.ajax({
		url: xmlPath,
		type: 'GET',
		dataType: 'json',
		timeout: 10000,
		success: function(jsondata)
		{
			var code;
			var name;
			var gb;
			for (ii = 0; ii < jsondata.Co.length;ii++ )
			{
				code = jsondata.Co[ii].cd;
				name = jsondata.Co[ii].nm;
				gb = jsondata.Co[ii].gb;
				if (datagb == '0')
				{
					results[results.length] = [ name + '[' + code + ']', code + gb]; //코드에 종목코드와 종목인지 EFT 인지 구분하는 구분자 같이 저장
				} else
				{
					if (datagb == gb)
					{
						results[results.length] = [name + '[' + code + ']', code + gb]; //코드에 종목코드와 종목인지 EFT 인지 구분하는 구분자 같이 저장
					}
				}
			}
		},
		error:function(jsondata)
		{
			//alert('error occurred');
		}
	});
}

function selectResult(item) {
	var text = '' + item.data,
		url = window.location.pathname,
		filename = url.substring(url.lastIndexOf('/')+1),
		gname = item.value.substr(0,item.value.indexOf('['));

	if (filename === 'SVD_comp_calendar.asp') {
		alert('종목(' + gname + ')을 선택했습니다.\n전체종목 보기를 클릭해서 전체종목 조회를 할 수 있습니다.');
		$('#gcd').val(text.substring(0,7));
		$('#gnm').val(gname);
		$('#stkGb').val(text.substring(0,7));
	} else {
		//alert(text.substring(0,7));
		$('#gicode').val(text.substring(0,7));
		$('#giname').val(gname);
		$('#stkGb').val(text.substring(7,text.length));
	}
	GoRefresh();

	//document.getElementById('debug').innerHTML = '종목명 : ' + item.value + ', 종목코드 : ' + text.substring(0,text.length-1) + ', 종목구분 : ' + text.substr(text.length-1,1) + '<br/>';
};

function displayValue(value, data) {
	var code = '' + data;
	return value.replace('[' + code.substring(0,7)+ ']','');
};

function stringValue(value, code) {
	var txt = $("#SearchText").val();
	code = value.replace('[' + code.substring(0,7)+ ']','');
	code = code.replace(txt,'<strong>'+txt+'</strong>');
	return code;
};

function showResult(value, data) {
	var code = '' + data;
	var name = stringValue(value, code);
	return '<span style="cursor:pointer;">'+name+'</span><span class="stnum">'+code.substring(1,7)+'</span>';
//	return '<a href="javascript:void(0);">'+name+'</a><span class="stnum">'+code.substring(1,7)+'</span>';
	//return '<span class="autosearchresult" style="color:black;">2' +  value.replace('[' + code.substring(0,7)+ ']','')  + ' [' + code.substring(0,7) + '] </span>';
};

function formatItem(item) {
	return item.data;
};