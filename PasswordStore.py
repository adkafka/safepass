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
        print(self)
        print("")
        print("Please enter the ID of the desired password: ")
        num_retries = 3
        while num_retries > 0:
            new_id = int(raw_input())
            ret_pass = self.get_pass(new_id)
            if ret_pass==False:
                print("Could not find password with that ID belonging to this domain.")
                print("Please try again with a valid ID")
            else:
                return ret_pass

            num_retries-=1

        return False

    def __repr__(self):
        ret = ""
        ret+="--------------------------\n"
        ret+="+ {}\n".format(self.name)
        ret+=" \\ Created: {}\n".format(time_str(self.created_on))
        ret+=" \\ Last Used: {}\n".format(time_str(self.last_accessed))
        self.passwords.sort(key=lambda r: r.last_accessed, reverse=True)
        for password in self.passwords:
            ret+=str(password)
        ret+=("--------------------------\n")

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

    def ls(self):
        domain_objs = []
        # Print every domain
        for _,val in self.db.iteritems():
            domain_objs.append(val)

        # Sort by when last accessed
        domain_objs.sort(key=lambda r: r.last_accessed,reverse=True)
        for domain in domain_objs:
            print(domain)

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
            sys.exit(1)

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
    matches = difflib.get_close_matches(search_str,list_options,cutoff=0.7)
    if len(matches)==0:
        return None
    return matches[0]
def now():
    return datetime.datetime.now()

def time_str(time_obj):
    return time_obj.strftime("%Y-%m-%d %H:%M")
