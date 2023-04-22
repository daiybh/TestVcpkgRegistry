# 这个函数有以下功能
# 遍历 ports 文件夹
# read all ports
# read all portfile.cmake
# get sections 'vcpkg_from_git' or 'vcpkg_from_github' or 'vcpkg_from_bitbucket'
# the sections include REPO REF SHA512 HEAD_REF
#  update REF SHA512  form REPO 

import pathlib,re

import argparse 
import requests

from checkbitbucket import getLastCommit

def parse_vcpkg_from(portfile,beginKey="vcpkg_from_github(",endKey="vcpkg_from_github("):
    metaDataList=[]
    end=0
    while True:
        begin = portfile.find(beginKey,end)
        if begin == -1:
            break

        begin += len(endKey)
        end = portfile.find(")", begin)
       

        interest = portfile[begin:end]
        splits = re.split(' |\n', interest)
        items = []
        for split in splits:
            split = split.strip()
            if len(split) > 0:
                items.append(split)

        if len(items) % 2 != 0:
            break

        ret = {}
        for i in range(0, len(items), 2):
            ret[items[i]] = items[i + 1]
        metaDataList.append(ret)
    return metaDataList
#https://api.bitbucket.org/2.0/repositories/id4tv/jpeg/commit
def github_get_latest_commit(repo, head):
    r = requests.get(f"https://api.github.com/repos/{repo}/commits/{head}", proxies={
                     'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'})
    j = r.json()
    return j['sha']

def bitbucket_get_last_commit(repo,head):
    #git@bitbucket.org:id4tv/jpeg.git
    name = repo.split('/')[-1].split('.')[0]
    return getLastCommit(repo_slug=name,head=head)

def parse_vcpkgGitForm(portfile):
    #githubMeta=parse_vcpkg_from(portfile)
    gitMeta=parse_vcpkg_from(portfile,beginKey='vcpkg_from_git(',endKey='vcpkg_from_git(')
    #bibucketMeta=parse_vcpkg_from(portfile,beginKey='vcpkg_from_bitbucket(',endKey='vcpkg_from_bitbucket(')
    allMeta=[]
    #allMeta.extend(githubMeta)
    allMeta.extend(gitMeta)
    #allMeta.extend(bibucketMeta)
    return allMeta


parser = argparse.ArgumentParser(description='Auto update vcpkg private registry repo')
parser.add_argument('-f', action='store_true', help="Force update all files, even the local portfile.cmake already up-to-date.") 
args = parser.parse_args() 

force_update = args.f

ports_folder = pathlib.Path("./ports")
for port in ports_folder.iterdir():
    vcpkg_json_path = port.joinpath("vcpkg.json")
    portfile_cmake_path = port.joinpath("portfile.cmake")
    if vcpkg_json_path.exists() and portfile_cmake_path.exists():
        print("Updating " + port.name)
        # Parse vcpkg_from_github
        portfile_str = portfile_cmake_path.read_text()
        github_meta = parse_vcpkgGitForm(portfile_str)
        if github_meta is None:
            continue
        for meta in github_meta:
            print(meta)
            cur_ref=meta['REF']
            latest_commit = bitbucket_get_last_commit(meta['URL'], meta['HEAD_REF'])
            if latest_commit ==cur_ref  and not force_update:
                print("- Already up-to-date.")
                continue

            # Calculate Latest SHA512
            #latest_sha512 = github_get_archive(github_repo, latest_commit)
            print(f"- Latest commit {latest_commit}")
            #print(f"- Latest sha512 = {latest_sha512}")

            # Update portfile.cmake
            #portfile_str = portfile_str.replace(github_sha, latest_sha512)
            portfile_str = portfile_str.replace(cur_ref, latest_commit)
            portfile_cmake_path.write_text(portfile_str)