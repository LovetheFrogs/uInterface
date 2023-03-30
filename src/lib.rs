use cpython::py_module_initializer;
use reqwest::Url;
use exitfailure::ExitFailure;
use serde_derive::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
struct Problem {
    pid: u16,
    num: u16,
    title: String,
    dacu: u32,
    mrun: u128,
    mmem: u128,
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

#[derive(Serialize, Deserialize, Debug)]
struct Submission {
    sid: i64,
    pid: u16,
    ver: u16,
    lan: u8,
    run: u64,
    mem: u128,
    rank: u16,
    sbt: u128,
    name: String,
    uname: String
}

#[derive(Serialize, Deserialize, Debug, PartialEq)]
struct UserSubmission {
    name: String,
    uname: String,
    subs: Vec<Vec<u64>>
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


async fn get_problem(num: u16) -> Result<Problem, ExitFailure> {
    let url = format!(
        "https://uhunt.onlinejudge.org/api/p/num/{}",
        num
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