package spider;


import java.util.ArrayList;
import java.util.List;

import org.htmlparser.Node;
import org.htmlparser.Parser;
import org.htmlparser.util.NodeIterator;
import org.htmlparser.util.ParserException;
import org.json.JSONArray;
import org.json.JSONObject;

import model.Major;
import model.School;
import us.codecraft.webmagic.Page;
import us.codecraft.webmagic.Site;
import us.codecraft.webmagic.processor.PageProcessor;
import util.EXCELUtil;
import util.XMLUtil;

public class Vinji_Spider implements PageProcessor {
	
	private Site site = Site.me().setDomain("school.163.com")
            .setSleepTime(3000)
            .setUserAgent(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31");

	public static final String URL_LIST = "http://school\\.163\\.com/special/0001124J/guoneischool_0\\d.html*";
    public static final String URL_POST = "http://school\\.163\\.com/\\d{2}/1008/\\d{2}/.*.html#f=dlist";
    private  String ENCODE = "GBK";
    private  int stage = 0;
    private int count = 0;
    public static boolean continueCatch = true;
    public List<String>requestList = new ArrayList<String>();
    public  List<School> schoolList = EXCELUtil.getSchoolList();
    
    public  Vinji_Spider(int stage) {
		// TODO Auto-generated constructor stub
    	
    	this.stage = stage;
    	
	}
    
    @Override
    public void process(Page page) {
        
    	if(count == 0){
    		page.addTargetRequests(requestList);
    		requestList.clear();
    		if(stage == 0){
				getAllSchoolNum(schoolList, page);
				System.out.println("stage 0");
			}
    		count ++;
    	}else{
	    	
			 if(stage == 1){
				
				setAllSchoolNum(schoolList, page);
				System.out.println("stage 1");
			}else if(stage ==2){
				page.addTargetRequests(requestList);
				getAllSchoolAndMajor(schoolList,page);
				System.out.println("stage 2");
			}
    	}
    }
    
    public void getAllSchoolNum(List<School> schoolList,Page page){
    	
    	
    	for(School school : schoolList){
	    	String request = "http://data.api.gkcx.eol.cn/soudaxue/querySpecialtyScore.html?messtype=jsonp&url_sign=querySpecialtyScore&provinceforschool=&schooltype=普通本科&page=&size=10&keyWord=" + school.getSchoolName() + "&schoolproperty=&schoolflag=211工程&schoolsort=&province=&fsyear=&fstype=&zhaoshengpici=&suiji=&callback=&";
	    	requestList.add(request);
    	}
    }
    
    public void setAllSchoolNum(List<School> schoolList,Page page){
    	
    	
    		String jsonString = page.getHtml().xpath("//body").toString();
			Parser parse = Parser.createParser(jsonString, ENCODE);
			
			try {
				
				for(NodeIterator i = parse.elements(); i.hasMoreNodes();)
				{
					Node node = i.nextNode();
					jsonString = node.toPlainTextString();
				}
				
				jsonString = jsonString.replace("&quot;", "\"");
				jsonString = jsonString.substring(3,jsonString.length()-3);
				JSONObject jb = new JSONObject(jsonString);
				if(jb.keySet().size()==2){
					JSONObject numObject = jb.getJSONObject("totalRecord");
					int num = numObject.getInt("num");
					//System.out.println("num:"+num + ",num/50=" + num/50);
					
					JSONArray jsonArray = (JSONArray)jb.get("school");
					School searchSchool = new School();
					for(int i = 0 ; i < 1; i++){
						
						
						searchSchool.setSchoolName(jsonArray.getJSONObject(i).getString("schoolname"));
					}
					for(int i = 1; i <= num/50 + 1; i ++){
						String request = "http://data.api.gkcx.eol.cn/soudaxue/querySpecialtyScore.html?messtype=jsonp&url_sign=querySpecialtyScore&provinceforschool=&schooltype=普通本科&page=" + i + "&size=50&keyWord=" + searchSchool.getSchoolName() + "&schoolproperty=&schoolflag=211工程&schoolsort=&province=&fsyear=&fstype=&zhaoshengpici=&suiji=&callback=&";
						requestList.add(request);
					}
				}
			} catch (ParserException e) {	
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
    	}
    	
    
    
    
    
    public void getAllSchoolAndMajor(List<School> schoolList, Page page){
    	
    	String jsonString = page.getHtml().xpath("//body").toString();
		Parser parse = Parser.createParser(jsonString, ENCODE);
		
		try {
			
			for(NodeIterator i = parse.elements(); i.hasMoreNodes();)
			{
				Node node = i.nextNode();
				jsonString = node.toPlainTextString();
			}
			
			jsonString = jsonString.replace("&quot;", "\"");
			jsonString = jsonString.substring(3,jsonString.length()-3);
			JSONObject jb = new JSONObject(jsonString);
			if(jb.keySet().size()==2){
				JSONArray jsonArray = (JSONArray)jb.get("school");
			
				for(int i = 0 ; i < jsonArray.length(); i++){
					
					School searchSchool = new School();
					searchSchool.setSchoolName(jsonArray.getJSONObject(i).getString("schoolname"));
					if(schoolList.indexOf(searchSchool)!=-1){
						
						School school = schoolList.get(schoolList.indexOf(searchSchool));
						List<Major> majorList = school.getMajorList();
						if(majorList == null)
							majorList = new ArrayList<Major>();
						Major major = new Major();
						
						
						school.setSchooleID(jsonArray.getJSONObject(i).getString("schoolid"));
						school.setSchoolName(jsonArray.getJSONObject(i).getString("schoolname"));
						major.setSpecialtyname(jsonArray.getJSONObject(i).getString("specialtyname"));
						major.setLocalProvince(jsonArray.getJSONObject(i).getString("localprovince"));
						major.setStudentType(jsonArray.getJSONObject(i).getString("studenttype"));
						major.setYear(jsonArray.getJSONObject(i).getString("year"));
						major.setBatch(jsonArray.getJSONObject(i).getString("batch"));
						major.setVar(jsonArray.getJSONObject(i).getString("var"));
						major.setVar_score(jsonArray.getJSONObject(i).getString("var_score"));
						major.setMax(jsonArray.getJSONObject(i).getString("max"));
						//major.setMin(jsonArray.getJSONObject(i).getString("min"));
						//System.out.println(jsonArray.getJSONObject(i).get("min"));
						major.setZyid(jsonArray.getJSONObject(i).getString("zyid"));
						major.setSeesigh(jsonArray.getJSONObject(i).getString("seesign"));
						major.setUrl(jsonArray.getJSONObject(i).getString("url"));
						
						if(!majorList.contains(major)){
							
							majorList.add(major);
						}else{
							
							majorList.remove(major);
							majorList.add(major);
						}
					}
				}
			}
			
			
			
		} catch (ParserException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	
     }

    @Override
    public Site getSite() {
        return site;
    }

	public boolean isContinueCatch() {
		return continueCatch;
	}

	public void setContinueCatch(boolean continueCatch) {
		this.continueCatch = continueCatch;
	}

    
}
