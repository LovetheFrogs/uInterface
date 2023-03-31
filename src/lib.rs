use cpython::{PyResult, Python, py_module_initializer, py_fn, ToPyObject, PyDict, PyObject, PyList};
use reqwest::Url;
use exitfailure::ExitFailure;
use serde_derive::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
struct Problem {
    pid: u16,
    num: u16,
    title: String,
    dacu: u32,
    mrun: u64,
    mmem: u64,
    nover: u16,
    sube: u16,
    noj: u16,
    inq: u16,
    ce: u16,
    rf: u16,
    re: u16,
    ole: u16,
    tle: u16,
    wa: u16,
    pe: u16,
    ac: u16,
    rtl: u16,
    status: u8,
    rej: i32,
}

impl ToPyObject for Problem {
    type ObjectType = PyDict;
    
    fn to_py_object(&self, py: Python) -> PyDict {
        let dict = PyDict::new(py);

        dict.set_item(py, "pid", self.pid).unwrap();
        dict.set_item(py, "num", self.num).unwrap();
        dict.set_item(py, "title", self.title.to_py_object(py)).unwrap();
        dict.set_item(py, "dacu", self.dacu).unwrap();
        dict.set_item(py, "mrun", self.mrun).unwrap();
        dict.set_item(py, "mmem", self.mmem).unwrap();
        dict.set_item(py, "nover", self.nover).unwrap();
        dict.set_item(py, "sube", self.sube).unwrap();
        dict.set_item(py, "noj", self.noj).unwrap();
        dict.set_item(py, "inq", self.inq).unwrap();
        dict.set_item(py, "ce", self.ce).unwrap();
        dict.set_item(py, "rf", self.rf).unwrap();
        dict.set_item(py, "re", self.re).unwrap();
        dict.set_item(py, "ole", self.ole).unwrap();
        dict.set_item(py, "tle", self.tle).unwrap();
        dict.set_item(py, "wa", self.wa).unwrap();
        dict.set_item(py, "pe", self.pe).unwrap();
        dict.set_item(py, "ac", self.ac).unwrap();
        dict.set_item(py, "rtl", self.rtl).unwrap();
        dict.set_item(py, "status", self.status).unwrap();
        dict.set_item(py, "rej", self.rej).unwrap();

        dict
    }
}

#[derive(Serialize, Deserialize, Debug)]
struct Submission {
    sid: i64,
    pid: u16,
    ver: u16,
    lan: u8,
    run: u64,
    mem: u64,
    rank: u16,
    sbt: u64,
    name: String,
    uname: String
}

impl ToPyObject for Submission {
    type ObjectType = PyDict;

    fn to_py_object(&self, py: Python) -> PyDict {
        let dict = PyDict::new(py);

        dict.set_item(py, "sid", self.sid).unwrap();
        dict.set_item(py, "pid", self.pid).unwrap();
        dict.set_item(py, "ver", self.ver).unwrap();
        dict.set_item(py, "lan", self.lan).unwrap();
        dict.set_item(py, "run", self.run).unwrap();
        dict.set_item(py, "mem", self.mem).unwrap();
        dict.set_item(py, "rank", self.rank).unwrap();
        dict.set_item(py, "sbt", self.sbt).unwrap();
        dict.set_item(py, "name", self.name.to_py_object(py)).unwrap();
        dict.set_item(py, "uname", self.uname.to_py_object(py)).unwrap();

        dict
    }
}

#[derive(Serialize, Deserialize, Debug, PartialEq)]
struct UserSubmission {
    name: String,
    uname: String,
    subs: Vec<Vec<u64>>
}

impl ToPyObject for UserSubmission {
    type ObjectType = PyDict;

    fn to_py_object(&self, py: Python) -> PyDict {
        let dict = PyDict::new(py);
        
        dict.set_item(py, "name", self.name.to_py_object(py)).unwrap();
        dict.set_item(py, "uname", self.uname.to_py_object(py)).unwrap();
        dict.set_item(py, "subs", self.subs.to_py_object(py)).unwrap();
        
        dict
    }
}

#[derive(Serialize, Deserialize, Debug)]
struct UserRank {
    rank: u32,
    old: u8,
    userid: u32,
    name: String,
    username: String,
    ac: u16,
    nos: u16,
    activity: Vec<u16>
}

impl ToPyObject for UserRank {
    type ObjectType = PyDict;

    fn to_py_object(&self, py: Python) -> PyDict {
        let dict = PyDict::new(py);

        dict.set_item(py, "rank", self.rank).unwrap();
        dict.set_item(py, "old", self.old).unwrap();
        dict.set_item(py, "userid", self.userid).unwrap();
        dict.set_item(py, "name", self.name.to_py_object(py)).unwrap();
        dict.set_item(py, "username", self.username.to_py_object(py)).unwrap();
        dict.set_item(py, "ac", self.ac).unwrap();
        dict.set_item(py, "nos", self.nos).unwrap();
        dict.set_item(py, "activity", self.activity.to_py_object(py)).unwrap();

        dict
    }
}

py_module_initializer!(u_interface, |py, m| {
    m.add(py, "__doc__", "Python module written in Rust to make requests to uHunt's API")?;
    m.add(py, "get_problem", py_fn!(py, get_problem_py(num: u16)))?;
    m.add(py, "get_submissions", py_fn!(py, get_submissions_py(pid: u16, start: u16, end: u16)))?;
    m.add(py, "get_user_submissions", py_fn!(py, get_user_subs_py(uid: u32, count: u16)))?;
    m.add(py, "get_ranking", py_fn!(py, get_ranking_py(uid: u32, above: u16, below: u16)))?;
    m.add(py, "get_uid", py_fn!(py, get_uid_py(uname: String)))?;
    m.add(py, "get_pdf_url", py_fn!(py, get_pdf_url_py(num: String)))?;
    Ok(())
});


async fn get_problem(num: u16) -> Result<Problem, ExitFailure> {
    let url = format!(
        "https://uhunt.onlinejudge.org/api/p/num/{}",
        num
    );

    let url = Url::parse(&*url)?;
    let prob = reqwest::get(url).await?.json::<Problem>().await?;

    Ok(prob)
}

async fn get_problem_by_pid(pid: u16) -> Result<Problem, ExitFailure> {
    let url = format!(
        "https://uhunt.onlinejudge.org/api/p/id/{pid}",
    );

    let url = Url::parse(&*url)?;
    let prob = reqwest::get(url).await?.json::<Problem>().await?;

    Ok(prob)
}

async fn get_submissions_problem(pid: u16, start: u16, end: u16) -> Result<Vec<Submission>, ExitFailure> {
    let url = format!(
        "https://uhunt.onlinejudge.org/api/p/rank/{pid}/{start}/{end}",
    );

    let url = Url::parse(&*url)?;
    let sub = reqwest::get(url).await?.json::<Vec<Submission>>().await?;

    Ok(sub)
}

async fn get_user_submissions(uid: u32, count: u16) -> Result<UserSubmission, ExitFailure> {
    let url = format!(
        "https://uhunt.onlinejudge.org/api/subs-user-last/{uid}/{count}"
    );

    let url = Url::parse(&*url)?;
    let usubs = reqwest::get(url).await?.json::<UserSubmission>().await?;

    Ok(usubs)
}

async fn get_ranking(uid: u32, above: u16, below: u16) -> Result<Vec<UserRank>, ExitFailure> {
    let url = format!(
        "https://uhunt.onlinejudge.org/api/ranklist/{uid}/{above}/{below}"
    );

    let url = Url::parse(&*url)?;
    let rank = reqwest::get(url).await?.json::<Vec<UserRank>>().await?;

    Ok(rank)
}

async fn get_uid_from_uname(uname: String) -> Result<u32, ExitFailure> {
    let url = format!(
        "https://uhunt.onlinejudge.org/api/uname2uid/{uname}"
    );

    let url = Url::parse(&*url)?;
    let uid = reqwest::get(url).await?.json::<u32>().await?;

    Ok(uid)
}

fn get_pdf_url_from_problem(num: String) -> String {
    let prelude = match num.len() {
        3 => &num[..1],
        4 => &num[..2],
        5 => &num[..3],
        _ => &num[..3],
    };

    format!("https://onlinejudge.org/external/{prelude}/{num}.pdf")

}


fn get_problem_py(_: Python<'_>, num: u16) -> PyResult<Problem> {
    let rt = tokio::runtime::Runtime::new().unwrap();
    let contents = rt.block_on(get_problem(num)).unwrap();

    Ok(contents)
}

fn get_problem_by_pid_py(_: Python<'_>, pid: u16) -> PyResult<Problem> {
    let rt = tokio::runtime::Runtime::new().unwrap();
    let contents = rt.block_on(get_problem_by_pid(pid)).unwrap();

    Ok(contents)
}

fn get_submissions_py(_: Python<'_>, pid: u16, start: u16, end: u16) -> PyResult<Vec<Submission>> {
    let rt = tokio::runtime::Runtime::new().unwrap();
    let contents = rt.block_on(get_submissions_problem(pid, start, end)).unwrap();
    
    Ok(contents)
}

fn get_user_subs_py(_: Python<'_>, uid: u32, count: u16) -> PyResult<UserSubmission> {
    let rt = tokio::runtime::Runtime::new().unwrap();
    let contents = rt.block_on(get_user_submissions(uid, count)).unwrap();
    
    Ok(contents)
}

fn get_ranking_py(_: Python<'_>, uid: u32, above: u16, below: u16) -> PyResult<Vec<UserRank>> {
    let rt = tokio::runtime::Runtime::new().unwrap();
    let contents = rt.block_on(get_ranking(uid, above, below)).unwrap();
    
    Ok(contents)
}

fn get_uid_py(_: Python<'_>, uname: String) -> PyResult<u32> {
    let mut rt = tokio::runtime::Runtime::new().unwrap();
    let mut contents = rt.block_on(get_uid_from_uname(uname)).unwrap();
    
    Ok(contents)
}

fn get_pdf_url_py(_: Python, num: String) -> PyResult<String> {
    Ok(get_pdf_url_from_problem(num))
}

#[cfg(test)]
mod tests {
    use super::*;
    use actix_rt::test;

    #[actix_rt::test]
    async fn test_get_a_problem() {
        let prob_462: Problem = get_problem(462).await.unwrap();
        assert_eq!(prob_462.pid, 403)
    }

    #[actix_rt::test]
    async fn test_get_problem_by_pid() {
        let prob_462: Problem = get_problem_by_pid(403).await.unwrap();
        assert_eq!(prob_462.num, 462)
    }

    #[actix_rt::test]
    async fn test_get_submissions() {
        let subs: Vec<Submission> = get_submissions_problem(403, 1, 2).await.unwrap();
        assert_eq!(subs[0].sid, 1065763);
    }

    #[actix_rt::test]
    async fn test_user_submissions() {
        let subs: UserSubmission = get_user_submissions(1589052, 1).await.unwrap();
        let vec: Vec<Vec<u64>> = vec![vec![28344490, 1587, 90, 360, 1680048279, 2, 3052]];
        let expected = UserSubmission {
            name: String::from("Marcos"),
            uname: String::from("LovetheFrogs"),
            subs: vec,
        };

        assert_eq!(expected, subs);
    }

    #[actix_rt::test]
    async fn test_get_ranking() {
        let rank = get_ranking(1589052, 1, 1).await.unwrap();
        assert_eq!(rank[0].name, String::from("abigail"));
    }

    #[actix_rt::test]
    async fn test_uid_from_uname() {
        assert_eq!(get_uid_from_uname(String::from("LovetheFrogs")).await.unwrap(), 1589052);
    }

    #[test]
    async fn test_get_pdf_url() {
        assert_eq!(get_pdf_url_from_problem(String::from("462")), String::from("https://onlinejudge.org/external/4/462.pdf"));
    }
}