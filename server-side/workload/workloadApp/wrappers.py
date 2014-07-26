

# wrapper for view
# redirects to privacy agreement if agreement has not been given
def user_agreement_to_terms_and_conditions_required(view):

	def redirectToTermsAndConditions(request):
		return HttpResponseRedirect('privacyAgreement?'+'url='+request.get_full_path())

	if user.student.agreedToTermnsAndConditions:
		return view
	else
		return redirectToTermsAndConditions