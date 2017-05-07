from __future__ import print_function
import datetime
import getpass
import time
import difflib


class Domain:
    def __init__(self,name):
        self.name = name
        self.created_on = now()
        self.last_accessed = now()
        self.passwords = []

    def add_password(self,pw,id_,notes=""):
        self.passwords.append(Password(pw,id_,notes))
        last_accessed = now()

    def get_pass(self,id_):
        for passwd in self.passwords:
            if passwd.id==id_:
                passwd.last_accessed = now()
                self.last_accessed = now()

                return passwd

        return False

    def select_password(self):
        print(self, end='')
        print(self.str_passwords())
        print("")
        print("Please enter the ID of the desired password: ")
        num_retries = 3
        while num_retries > 0:
            try:
                new_id = int(raw_input())
                ret_pass = self.get_pass(new_id)
                if ret_pass==False:
                    print("Could not find password with that ID belonging to this domain.")
                    print("Please try again with a valid ID")
                else:
                    return ret_pass
            except ValueError:
                print("Must input valid integer, try again")

            num_retries-=1

        return False

    def __repr__(self):
        ret = ""
        ret+="--------------------------\n"
        ret+="+ {}\n".format(self.name)
        ret+=" \\ Created: {}\n".format(time_str(self.created_on))
        ret+=" \\ Last Used: {}\n".format(time_str(self.last_accessed))
        ret+=" \\ Number of PWs: {}\n".format(len(self.passwords))

        return ret
    
    def str_passwords(self):
        ret = ""
        self.passwords.sort(key=lambda r: r.last_accessed, reverse=True)
        for password in self.passwords:
            ret+=str(password)

        return ret


class Password:
    def __init__(self,password,id_,notes=""):
        self.password = password
        self.created_on = now()
        self.last_accessed = now()
        self.id = id_
        self.notes=notes

    def __repr__(self):
        ret = ""
        ret+="    +\n"
        ret+="    \\ ID: {}\n".format(self.id)
        ret+="    \\ Created: {}\n".format(time_str(self.created_on))
        ret+="    \\ Last Used: {}\n".format(time_str(self.last_accessed))
        if self.notes:
            ret+="    \\ Notes: {}\n".format(self.notes)

        return ret


class PasswordStore:
    def __init__(self):
        # Dictionary Domain_name -> Domain_obj
        self.db = {}
        self.id = 1

    def add(self,domain,notes=""):
        print("Adding password to domain: %s"%domain)
        pw = self.get_password("Enter password to add:")
        if not self.have_domain(domain):
            self.db[domain] = Domain(domain)

        self.db[domain].add_password(pw,self.new_id(),notes)

    # TODO, add domain specific ls
    def ls(self):
        # Sort by when last accessed
        self.db.values().sort(key=lambda r: r.last_accessed,reverse=True)
        for domain in self.db.values():
            print(domain)

    def search(self,phrase):
        all_notes = []
        all_passwords = []
        for dom in self.db.values():
            for pw in dom.passwords:
                all_notes.append(pw.notes)
                all_passwords.append((dom,pw))

        matches = difflib.get_close_matches(phrase,all_notes,cutoff=0.6,n=1)
        # Find the match
        try:
            if len(matches)==0:
                print("Could not find a password who's note is similar to query: {}".format(phrase))
                return False
            idx = all_notes.index(matches[0])
            tupl = all_passwords[idx]
            tupl[0].last_accessed = now()
            tupl[1].last_accessed = now()

            print("Found password: ")
            print(tupl[0])
            print(tupl[1])
            print(tupl[1].password)

            return True

        except ValueError:
            print("Could not find a password who's note is similar to query: {}".format(phrase))
            return False



    def get(self,domain):
        domain_names = self.db.keys()
        best_domain = get_close_string(domain_names,domain)
        # Couldn't find
        if best_domain==None:
            print("Could not find domain close to string: '{}'".format(domain))
            return False

        chosen_pw = self.db[best_domain].select_password()
        if chosen_pw==False:
            print("Could not find password, exiting")
            return False

        print(chosen_pw.password)

        return True



    ####################
    ## HELPER METHODS ##
    ####################
    def have_domain(self,domain):
        if self.db.has_key(domain):
            # Update last_accessed
            self.db[domain].last_accessed = now()
            return True
        return False

    def get_password(self,ask="Enter password"):
        return getpass.getpass(prompt=ask)

    def new_id(self):
        r = self.id
        self.id+=1
        return r

def get_close_string(list_options,search_str):
    matches = difflib.get_close_matches(search_str,list_options,cutoff=0.7,n=1)
    if len(matches)==0:
        return None
    return matches[0]
def now():
    return datetime.datetime.now()

def time_str(time_obj):
    return time_obj.strftime("%Y-%m-%d %H:%M")
