from generate_data import generate_patients
from generate_data import data
from datetime import datetime
from datetime import timedelta
from random import randint

class calendar:
    def __init__(self):
        self.weeks = {"Mo":[], "Tu":[], "We":[], "Th":[], "Fr":[]}
        self.days = ["Mo", "Tu", "We", "Th", "Fr"]
        self.day_ind = 0
        self.intervals = [[interval(8, 0, 20, 0)]]

    def new_day(self):
        self.day_ind = (self.day_ind + 1) % 5

    def get_day(self):
        return self.days[self.day_ind]

    def add_appointment(self, days_from_now, start_h, start_m, end_h, end_m):
        for ind, inter in enumerate(self.intervals[days_from_now]):
            if inter.contains(start_h, start_m, end_h, end_m):
                i1 = interval(inter.start_h, inter.start_m, start_h, start_m)
                i2 = interval(end_h, end_m, inter.end_h, inter.end_m)
                l1 = i1.makes_sense()
                l2 = i2.makes_sense()

                if l1 and l2:
                    self.intervals[days_from_now].append(i2)
                    self.intervals[days_from_now][ind] = i1
                elif l1:
                    self.intervals[days_from_now][ind] = i1
                elif l2:
                    self.intervals[days_from_now][ind] = i2
                else:
                    self.intervals[days_from_now].remove(inter)

                break

    def add_appointment_interv(self, days_from_now, interv):
        for ind, inter in enumerate(self.intervals[days_from_now]):
            if inter.contains(interv.start_h, interv.start_m, interv.end_h, interv.end_m):
                i1 = interval(inter.start_h, inter.start_m, interv.start_h, interv.start_m)
                i2 = interval(interv.end_h, interv.end_m, inter.end_h, inter.end_m)
                l1 = i1.makes_sense()
                l2 = i2.makes_sense()

                if l1 and l2:
                    self.intervals[days_from_now].append(i2)
                    self.intervals[days_from_now][ind] = i1
                elif l1:
                    self.intervals[days_from_now][ind] = i1
                elif l2:
                    self.intervals[days_from_now][ind] = i2
                else:
                    self.intervals[days_from_now].remove(inter)

                break
        
    def expand_by_n_days(self, days):
        for i in range(days):
            self.intervals.append([interval(8, 0, 20, 0)])

    def get_free_intervals(self, days_from_now):
        diff = days_from_now - len(self.intervals)+1
        if (diff > 0):
            self.expand_by_n_days(diff)

        return self.intervals[days_from_now]

    def __str__(self):
        d = self.day_ind
        s = ""
        for day in self.intervals:
            s += "-----------------\n"
            s += self.days[d] + "\n"
            d = (d + 1) % 5
            for inter in day:
                s += str(inter) + "\n"
            s += "-----------------\n"
            s += "\n"
        return s
    
    def clear(self):
        self.day_ind = 0
        self.intervals = [[interval(8, 0, 20, 0)]]
        

class interval:
    def __init__(self, start_h, start_m, end_h, end_m):
        self.start = timedelta(hours=start_h, minutes=start_m)
        self.end = timedelta(hours=end_h, minutes=end_m)
        self.start_h = start_h
        self.start_m = start_m
        self.end_h = end_h
        self.end_m = end_m

    def contains(self, start_h, start_m, end_h, end_m):
        start = timedelta(hours=start_h, minutes=start_m)
        end = timedelta(hours=end_h, minutes=end_m)
        diff_s = start - self.start
        diff_end = self.end - end
        return diff_s.total_seconds() >= 0 and diff_end.total_seconds() >= 0
    
    def get_minutes(self):
        diff = self.end-self.start
        return int(diff.total_seconds()//60)
    
    def makes_sense(self):
        diff = self.end - self.start
        return diff.total_seconds() != 0
    
    def get_minutes_of_today(self):
        return (self.start_h*60)+self.start_m,(self.end_h*60)+self.end_m
    
    def __str__(self) -> str:
        return str(int(self.start.total_seconds()//3600)) + ":" + str((self.start.seconds//60)%60) + " -> " + str(int(self.end.total_seconds()//3600)) + ":" + str((self.end.seconds//60)%60)


def decide_machine(patient):
    if patient.type in ["Craniospinal", "Breast special", "Abdomen"]:
        return tb1, "TB1"
    elif patient.type in ["Crane", "Whole Brain"]:
        return tb2, "TB2"
    elif patient.type == "Breast":
        x = randint(1,10)
        if x <= 4:
            return tb2, "TB2"
        else:
            return u, "U"
    elif patient.type == "Head & neck":
        return vb1, "VB1"
    elif patient.type == "Lung":
        x = randint(1, 10)
        if x <= 8:
            return vb1, "VB1"
        else:
            return vb2, "VB2"
    else:
        return vb2, "VB2"


def give_appointment_times(patient):
    #we need to appoint the person for n consecutive days for a given amount of time
    days = patient.fraction
    time = patient.time
    c = decide_machine(patient)
    name = c[1]
    c = c[0]
    out = []
    rem_days = days
    days_elapsed = 0
    day_nr = 0

    while rem_days > 0:

        impossible = len(c.get_free_intervals(day_nr))
        # contains_exactly = time in c.get_free_intervals(day_nr)
        for i, n in enumerate(c.get_free_intervals(day_nr)):
            mins = n.get_minutes()
            if mins < time:
                impossible -= 1
                continue
            
            if mins == time:
                # out.append(c.intervals[day_nr][i])
                inter = interval(c.intervals[day_nr][i].start_h, c.intervals[day_nr][i].start_m, c.intervals[day_nr][i].start_h+((c.intervals[day_nr][i].start_m+time)//60), (c.intervals[day_nr][i].start_m+time)%60)
                out.append(inter.get_minutes_of_today())
                break
            
            inter = interval(c.intervals[day_nr][i].start_h, c.intervals[day_nr][i].start_m, c.intervals[day_nr][i].start_h+((c.intervals[day_nr][i].start_m+time)//60), (c.intervals[day_nr][i].start_m+time)%60)
            out.append(inter.get_minutes_of_today())
            c.add_appointment_interv(day_nr, inter)
            break
            
        if impossible <= 0:
            days_elapsed += days-rem_days
            out = []
            rem_days = days

        day_nr += 1
        rem_days -= 1
    for i in range(days_elapsed):
        out.insert(0, None)
    return name, out, patient.name, patient.id, patient.type

def decide_machine_custom(patient_type):
    if patient_type in ["Craniospinal", "Breast special", "Abdomen"]:
        return tb1, "TB1"
    elif patient_type in ["Crane", "Whole Brain"]:
        return tb2, "TB2"
    elif patient_type == "Breast":
        x = randint(1,10)
        if x <= 4:
            return tb2, "TB2"
        else:
            return u, "U"
    elif patient_type == "Head & neck":
        return vb1, "VB1"
    elif patient_type == "Lung":
        x = randint(1, 10)
        if x <= 8:
            return vb1, "VB1"
        else:
            return vb2, "VB2"
    else:
        return vb2, "VB2"

def give_appointment_times_custom(patient_fraction, patient_time, patient_name, patient_id, patient_type):
    #we need to appoint the person for n consecutive days for a given amount of time
    days = patient_fraction
    time = patient_time
    c = decide_machine(patient_type)
    name = c[1]
    c = c[0]
    out = []
    rem_days = days
    days_elapsed = 0
    day_nr = 0

    while rem_days > 0:

        impossible = len(c.get_free_intervals(day_nr))
        # contains_exactly = time in c.get_free_intervals(day_nr)
        for i, n in enumerate(c.get_free_intervals(day_nr)):
            mins = n.get_minutes()
            if mins < time:
                impossible -= 1
                continue
            
            if mins == time:
                # out.append(c.intervals[day_nr][i])
                inter = interval(c.intervals[day_nr][i].start_h, c.intervals[day_nr][i].start_m, c.intervals[day_nr][i].start_h+((c.intervals[day_nr][i].start_m+time)//60), (c.intervals[day_nr][i].start_m+time)%60)
                out.append(inter.get_minutes_of_today())
                break
            
            inter = interval(c.intervals[day_nr][i].start_h, c.intervals[day_nr][i].start_m, c.intervals[day_nr][i].start_h+((c.intervals[day_nr][i].start_m+time)//60), (c.intervals[day_nr][i].start_m+time)%60)
            out.append(inter.get_minutes_of_today())
            c.add_appointment_interv(day_nr, inter)
            break
            
        if impossible <= 0:
            days_elapsed += days-rem_days
            out = []
            rem_days = days

        day_nr += 1
        rem_days -= 1
    for i in range(days_elapsed):
        out.insert(0, None)
    return name, out, patient_name, patient_id, patient_type

tb1 = calendar()
tb2 = calendar()
vb1 = calendar()
vb2 = calendar()
u = calendar()

def get_times():
    tb1.clear()
    tb2.clear()
    vb1.clear()
    vb2.clear()
    u.clear()
    patients = generate_patients(200)
    times = []
    for pat in patients:
        x = give_appointment_times(pat)
        times.append(x)
    # print(pat)
        # for z in x:
        #     print(z)
        # return times
    return times

# print(x[0], x[1:])
        # print(z)
# print(times)
    
# c.add_appointment(0, 6, 30, 7, 0)

# xl = give_appointment_times(30, 3)
# for x in xl:
#     print(x)

# print(c)