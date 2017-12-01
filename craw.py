import bs4,requests,sqlite3,time,multiprocessing
def craw(stuid):
    day = time.strftime("%Y-%m-%d", time.localtime())
    conn = sqlite3.connect('datas_'+day+'.db')
    sqlexec = conn.cursor()
    value = []
    url = "http://ecard.swust.edu.cn/web/admin/ecardrules;jsessionid=66C1FF6AA93810DD5DDCEB67D2B62D0?p_p_id=accounttransdtl&p_p_action=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_pos=1&p_p_col_count=5&_accounttransdtl_struts_action=%2Fext%2Faccounttransdtl_queryresult"
    payload = {"custId": "", "stuempno": stuid, "queryaccountdtl_begindate": day, "queryaccountdtl_enddate": day}
    r = requests.post(url, data=payload)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    if soup.tbody:
        sqlCreatTable = "create table stu_" + str(stuid) + " (name varchar(255),time_day varchar(255),time_min varchar(255),type varchar(255),consume varchar(255),remainder varchar(255));"
        sqlexec.execute(sqlCreatTable)
        for i in soup.tbody.find_all("td"):
            value.append(i.string)
        for count in range(len(value)/8):
            sqlIncertValue = "INSERT INTO stu_" + str(stuid) + " (name,time_day,time_min,type,consume,remainder) VALUES ('" + value[3+8*count] + "', '" + value[0+8*count] + "','" + value[1+8*count] + "', '" + value[4+8*count] + "','" + value[6+8*count] + "','" + value[7+8*count] + "')"
            sqlexec.execute(sqlIncertValue)

        print "crawing:"+str(stuid)
    else:
        print str(stuid)+" is not exist."
    conn.commit()
    conn.close()
if __name__=="__main__":
    start = time.clock()
    pool = multiprocessing.Pool(processes=16)
    pool.map_async(craw,range(5120170101,5120177300,1))
    pool.close()
    pool.join()
    end=time.clock()
    print "use: %f s"%(end-start)
