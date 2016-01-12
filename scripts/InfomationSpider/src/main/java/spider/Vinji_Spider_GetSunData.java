package spider;

import java.util.ArrayList;
import java.util.List;

import org.htmlparser.Node;
import org.htmlparser.NodeFilter;
import org.htmlparser.Parser;
import org.htmlparser.filters.NodeClassFilter;
import org.htmlparser.tags.LinkTag;
import org.htmlparser.tags.TableColumn;
import org.htmlparser.tags.TableRow;
import org.htmlparser.tags.TableTag;
import org.htmlparser.util.NodeIterator;
import org.htmlparser.util.NodeList;
import org.htmlparser.util.ParserException;

import dao.SchoolDAO;
import model.StoreageComment;
import model.StoreageMajor;
import model.StoreageSchool;
import us.codecraft.webmagic.Page;
import us.codecraft.webmagic.Site;
import us.codecraft.webmagic.processor.PageProcessor;
import util.SQLUtil;

public class Vinji_Spider_GetSunData implements PageProcessor {
	
	private Site site = Site.me().setDomain("school.163.com")
            .setSleepTime(3000)
            .setUserAgent(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31");
	
	public static final String URL_LIST = "http://gaokao.chsi.com.cn/zyk/pub/myd/specAppraisalTop.action*";
    public static final String URL_POST = "http://gaokao\\.chsi\\.com\\.cn/zyk/pub/myd/specAppraisalTopMore\\.action*";
    private static String ENCODE = "GBK";
    public static List<StoreageSchool> schoolList = new ArrayList<StoreageSchool>();
    public static boolean continueCatch = true;
    
    @Override
    public void process(Page page) {
        
    		if(page.getUrl().regex(URL_LIST).match() || page.getUrl().toString().equals("http://gaokao.chsi.com.cn/zyk/pub/myd/specAppraisalTop.action?zgsx=211&start=0")){

    	    	if(continueCatch){
    	    		
		    		 page.addTargetRequests(page.getHtml().xpath("//div[@class=\"pagebox clearfix\"]").links().all());
		    		 String majorInformations = page.getHtml().xpath("//div[@id='queryResult']/table").toString();
		    		 Parser parse = Parser.createParser(majorInformations, ENCODE);
		    		
						try {
							NodeFilter filter = new NodeClassFilter(TableTag.class);  
			    	        NodeList nodeList;
							nodeList = parse.parse(filter);
							  for(int i = 0; i < nodeList.size(); ++i){  
				    	            if(nodeList.elementAt(i) instanceof TableTag){  
				    	                TableTag tag = (TableTag) nodeList.elementAt(i);  
				    	                TableRow[] rows = tag.getRows();  
				    	  
				    	                for (int j = 0; j < rows.length; ++j) {  
				    	                    TableRow row = (TableRow) rows[j];  
				    	                    TableColumn[] columns = row.getColumns();  
				    	                    for (int k = 0; k < columns.length; ++k) {  
				    	                        String info = columns[k].toPlainTextString().trim();  
				    	                        if(info.equals("更多")){
				    	                        	NodeList linkList = columns[k].getChildren();
				    	                        	LinkTag linkTag = (LinkTag) linkList.elementAt(1);
				    	                        	String link = linkTag.extractLink();
				    	                        	link = link.replace("&amp;", "&");
				    	                        	
				    	                        	page.addTargetRequest(link);
				    	                        }
				    	                         
				    	                    }// end for k  
				    	                }// end for j  
				    	            }  
				    	        } 
						} catch (ParserException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
		    	        
		    	      
		            
		             
    	    	}
	    	}else{

	    		try {
	    			StoreageSchool school = new StoreageSchool();
	    			String schoolName = page.getHtml().xpath("//div[@class='main']/h2").toString();
	        		Parser parse = Parser.createParser(schoolName, ENCODE);
	        		
	    			for(NodeIterator i = parse.elements(); i.hasMoreNodes();)
					{
						Node node = i.nextNode();
						schoolName = node.toPlainTextString();
					}
	    			schoolName = schoolName.split(" ")[0];
	    			school.setSchoolName(schoolName);
	    			
	    			String majorInformations = page.getHtml().xpath("//div[@id='queryResult']/table").toString();
	    			parse = Parser.createParser(majorInformations, ENCODE);
	    			NodeFilter filter = new NodeClassFilter(TableTag.class);  
	    	        NodeList nodeList = parse.parse(filter);
	    	        
	    	        for(int i = 0; i < nodeList.size(); ++i){  
	    	            if(nodeList.elementAt(i) instanceof TableTag){  
	    	                TableTag tag = (TableTag) nodeList.elementAt(i);  
	    	                TableRow[] rows = tag.getRows();  
	    	  
	    	                for (int j = 1; j < rows.length; ++j) {  
	    	                    TableRow row = (TableRow) rows[j];  
	    	                    TableColumn[] columns = row.getColumns();  
	    	                    StoreageMajor major = new StoreageMajor();
	    	                    StoreageComment comment = new StoreageComment();
	    	                    String majorName = columns[0].toPlainTextString().trim();
	    	                    if(majorName.equals(""))
	    	                    	break;
	    	                    major.setMajorName(majorName);
	    	                    major.getComments().add(comment);
	    	                    school.getMajors().add(major);
	    	                    for (int k = 0; k < columns.length; ++k) {  
	    	                        String info = columns[k].toPlainTextString().trim();
	    	                        info = info.split("\n")[0];
	    	                        int index = info.indexOf("(");
	    	                        
	    	                        if(index!=-1){
	    	                        	info =  info.substring(0,index);
	    	                        	switch(k){
	    	                        		case 1:comment.setComprehensiveScore(Double.parseDouble(info));break;
	    	                        		case 2:comment.setDealScore(Double.parseDouble(info));break;
	    	                        		case 3:comment.setTeachingScore(Double.parseDouble(info));break;
	    	                        		case 4:comment.setWorkScore(Double.parseDouble(info));break;
	    	                        	}
	    	                        	
	    	                        }
	    	                    }// end for k  
	    	                }// end for j  
	    	            }  
	    	        }  
	    			/*
	    			String source = 
	    			parse = Parser.createParser(source, ENCODE);
	    			
	    			for(NodeIterator i = parse.elements(); i.hasMoreNodes();)
					{
						Node node = i.nextNode();
						source = node.toPlainTextString();
					}
	    			school.setSource(source);
	    			String content = page.getHtml().xpath("//div[@id='endText']").toString();
	    			
	    			parse = Parser.createParser(content, ENCODE);
	    			StringBuffer contentBuffer = new StringBuffer("");
	    			for(NodeIterator i = parse.elements(); i.hasMoreNodes();)
					{
						Node node = i.nextNode();
						contentBuffer.append(node.toPlainTextString());
					}
	    			school.setBody(contentBuffer.toString());
	    			String date = page.getHtml().xpath("//div[@class='ep-time-soure cDGray']")
	                        .regex("\\d{4}-\\d{2}-\\d{2}\\s\\d{2}:\\d{2}:\\d{2}").toString();
	    			
	    			school.setDate(date);
	    			*/
	    			schoolList.add(school);
	    			
	    			if(schoolList.size()>50){
	    				dealSchoolList();
	    				
	    			}
	    		
//	    			page.putField("school",school);
				} catch (ParserException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
	    		System.out.println("Catch status :" + continueCatch);
	    		System.out.println("schoolList size  :" + schoolList.size());
	    	}
    	
    	
    	
    }

    public synchronized void dealSchoolList(){
    	
    	SchoolDAO.saveComment(schoolList);
		
		schoolList.clear();
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
