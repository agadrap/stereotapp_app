# Generated by Django 2.1.7 on 2019-03-19 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnswersPersonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_personal', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AnswersStereo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_stereo', models.IntegerField(choices=[(1, 'Female'), (2, 'Male')])),
            ],
        ),
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('continent', models.IntegerField(choices=[(1, 'Europe'), (2, 'North America'), (3, 'South America'), (4, 'Asia'), (5, 'Africa'), (6, 'Australia & Oceania'), (7, 'Antarctica')], default=1, verbose_name='Continent')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100, null=True, verbose_name='Country')),
                ('continent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Continent')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Stranger', max_length=64, verbose_name='Name')),
                ('gender', models.IntegerField(choices=[(1, 'Female'), (2, 'Male')], verbose_name='Gender')),
                ('email', models.CharField(max_length=200, null=True, verbose_name='E-mail')),
                ('share_stats', models.BooleanField(default=False, verbose_name='Statistics')),
                ('continent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Continent', verbose_name='Continent')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Country', verbose_name='Country')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='StereotypeQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300)),
            ],
        ),
        migrations.AddField(
            model_name='answersstereo',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Participant'),
        ),
        migrations.AddField(
            model_name='answersstereo',
            name='question_stereo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.StereotypeQuestions'),
        ),
        migrations.AddField(
            model_name='answerspersonal',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Participant'),
        ),
        migrations.AddField(
            model_name='answerspersonal',
            name='question_personal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.PersonalQuestion'),
        ),
    ]
