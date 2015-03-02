function expand_title(page_num,num_on_page)
{
    var spans=document.getElementsByTagName("span");
    var i;
    for(i=0;i<spans.length;i++)
    {
        if(spans[i].getAttribute("num")==page_num+"_"+num_on_page)
        {
            spans[i].style.display="none";
            break;
        }
    }
    document.getElementById(page_num+"_"+num_on_page+"_full").style.display="inline";
}

function show_page(i)
{
    var old_page, new_page, buttons;
    old_page=document.getElementById("page_"+curr_page);
    old_page.style.display="none";
    
    new_page=document.getElementById("page_"+i);
    new_page.style.display="block";
    curr_page=i;
    
    buttons=document.getElementsByClassName("page_button");
    for(var j=0;j<buttons.length;j++)
        buttons[j].style.background="#aaaaaa"
    buttons[parseInt(i)-1].style.background='#888888';
    
    document.getElementById("prints_shown").innerHTML=((parseInt(i)-1)*prints_per_page+1)+"-"+(Math.min(parseInt(i)*prints_per_page, max_num));
    
    document.getElementById("curr_page_span").innerHTML=i;
}

function show_sorting(sorting)
{
    var links=document.getElementsByClassName("sort_link");
    for(var i=0;i<links.length;i++)
        links[i].style.fontWeight="normal";
    document.getElementById("sort_"+sorting).style.fontWeight="bold";
}

function show_collection(collection)
{
    var links=document.getElementsByClassName("sort_collection");
    for(var i=0;i<links.length;i++)
        links[i].style.fontWeight="normal";
    document.getElementById("collection_"+collection).style.fontWeight="bold";
}